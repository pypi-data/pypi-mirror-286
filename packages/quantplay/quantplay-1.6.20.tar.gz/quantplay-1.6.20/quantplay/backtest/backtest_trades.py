import numpy as np
import pandas as pd
import copy
from datetime import timedelta

from quantplay.reporting.strategy_report import StrategyReport

from quantplay.utils.constant import (
    TickInterval,
    StrategyType,
)
from quantplay.utils.constant import Constants


class Backtesting:
    def __init__(self, market):
        self.market_data = []
        self.market = market

    def load_data(self, symbols_by_security_type, interval, **kwargs):
        self.market_data = self.market.data(
            interval=interval,
            symbols_by_security_type=symbols_by_security_type,
            **kwargs,
        )

        self.market_data.loc[:, "tradingsymbol"] = self.market_data.symbol
        self.market_data["date"] = pd.to_datetime(self.market_data.date)
        self.market_data["date_only"] = self.market_data.date.dt.date
        self.market_data["date_only"] = pd.to_datetime(self.market_data.date_only)

        self.business_days_df = (
            self.market_data[["date_only"]]
            .sort_values(["date_only"])
            .groupby(["date_only"])
            .first()
            .reset_index()
        )

    def add_time(self, trades, column_time_tuple=None, holding_days=0):
        if not column_time_tuple:
            raise Exception(
                "column_time_tuple should be like ('column_name', 'hh:mm') e.g. ('exit_time', '15:29')"
            )
        time_column, time_value = column_time_tuple
        hour, minute = [int(a) for a in time_value.split(":")]

        if holding_days > 0:
            self.business_days_df.loc[
                :, "next_business_date_only"
            ] = self.business_days_df.date_only.shift(-holding_days)

            trades = pd.merge(
                trades,
                self.business_days_df,
                how="left",
                left_on=["date_only"],
                right_on=["date_only"],
            )
            trades.loc[:, time_column] = trades.next_business_date_only

            trades.loc[:, time_column] = trades[time_column].apply(
                lambda x: x.replace(hour=hour, minute=minute)
            )
        else:
            trades.loc[:, time_column] = trades.date.apply(
                lambda x: x.replace(hour=hour, minute=minute)
            )

        return trades[~trades[time_column].isna()]

    def add_intraday_metrics(self, entry_time, exit_time):
        self.market_data.loc[:, "price_column"] = self.market_data.close

        condition = (
            self.market_data.date.dt.time <= pd.to_datetime(entry_time).time()
        ) | (self.market_data.date.dt.time > pd.to_datetime(exit_time).time())
        self.market_data.loc[:, "price_column"] = np.where(
            condition, np.nan, self.market_data.price_column
        )

        self.market_data.loc[:, "intraday_high"] = self.market_data.groupby(
            ["symbol", "date_only"]
        ).price_column.transform(max)
        self.market_data.loc[:, "intraday_low"] = self.market_data.groupby(
            ["symbol", "date_only"]
        ).price_column.transform(min)

    def merge_columns(self, trades, columns=[], time_column_name=None):
        for column in columns:
            if column in trades.columns:
                trades = trades.drop([column], axis=1)

        self.market_data.loc[:, time_column_name] = self.market_data.date
        trades = pd.merge(
            trades,
            self.market_data[[time_column_name, "tradingsymbol"] + columns],
            how="left",
            left_on=["tradingsymbol", time_column_name],
            right_on=["tradingsymbol", time_column_name],
        )
        return trades

    def validate_trades(
        self,
        trades,
        columns_to_validate=[
            "transaction_type",
            "strategy_type",
            "exit_time",
            "tag",
            "uuid",
        ],
    ):

        if "transaction_type" in columns_to_validate:
            transaction_types = list(trades.transaction_type.unique())
            assert len(transaction_types) <= 2
            assert set(transaction_types).issubset({"BUY", "SELL"})

        if "strategy_type" in columns_to_validate:
            strategy_types = list(trades.strategy_type.unique())
            assert len(strategy_types) == 1
            assert strategy_types[0] in [
                StrategyType.intraday,
                StrategyType.overnight,
            ]

        if "exit_time" in columns_to_validate:
            assert "exit_time" in trades.columns, "Exit time must be provided in trades"

        if "tag" in columns_to_validate:
            assert "tag" in trades.columns

        if "uuid" in columns_to_validate:
            assert "uuid" in trades.columns

    def backtest(self, trades, interval="minute"):
        security_types = list(trades.security_type.unique())
        symbols_by_security_type = {}
        for security_type in security_types:
            symbols_by_security_type[security_type] = list(
                trades[trades.security_type == security_type].tradingsymbol.unique()
            )

        trades.loc[:, "date_only"] = pd.to_datetime(trades.date.dt.date)

        self.load_data(symbols_by_security_type, interval)

        return self.evaluate_performance(trades, interval, tag="testing")

    def filter_trigger_orders(self, trades, interval):
        columns = trades.columns
        if "validity" not in columns or "trigger_price" not in columns:
            return trades

        order_validity = trades.validity.unique()
        assert len(order_validity) == 1
        order_validity = order_validity[0]

        tick_size = TickInterval.get_interval_seconds(interval)
        if int(order_validity / tick_size) != order_validity / tick_size:
            raise Exception(
                "Invalid order validity {} for interval {}".format(
                    order_validity, interval
                )
            )

        num_ticks = int(order_validity / tick_size)
        self.market_data.loc[:, "window_max_price"] = (
            self.market_data.high.rolling(num_ticks).max().shift(-num_ticks)
        )
        self.market_data.loc[:, "window_min_price"] = (
            self.market_data.low.rolling(num_ticks).min().shift(-num_ticks)
        )

        trades = self.merge_columns(
            trades,
            columns=["window_max_price", "window_min_price"],
            time_column_name="entry_time",
        )

        trades = trades[
            (
                (trades.transaction_type == "SELL")
                & (trades.window_min_price < trades.trigger_price)
            )
            | (
                (trades.transaction_type == "BUY")
                & (trades.window_max_price > trades.trigger_price)
            )
        ]
        trades.loc[:, "entry_price"] = trades.trigger_price

        return trades

    def evaluate_performance(self, trades_df, interval, tag=None, args={}):
        """
        input : pandas dataframe
        columns : tradingsymbol, trade_time, stoploss, exit_time
        """
        trades = copy.deepcopy(trades_df)
        trades.loc[:, "original_date"] = trades.date

        self.market_data.loc[:, "entry_price"] = self.market_data.close
        trades = self.merge_columns(
            trades, columns=["entry_price"], time_column_name="entry_time"
        )

        self.market_data.loc[:, "close_price"] = self.market_data.close
        trades = self.merge_columns(
            trades, columns=["close_price"], time_column_name="exit_time"
        )

        trades = self.filter_trigger_orders(trades, interval)

        Constants.logger.info(
            "Dropping {} trades because entry price is not available".format(
                trades[trades.entry_price.isna()][["tradingsymbol", "date"]]
            )
        )
        trades = trades[trades.entry_price > 0]
        trades.loc[:, "entry_price"] = trades.entry_price.astype(float)
        Constants.logger.info(
            "Dropping {} trades because close price is not available".format(
                trades[trades.close_price.isna()][["tradingsymbol", "date"]]
            )
        )
        trades = trades[trades.close_price > 0]
        trades.loc[:, "close_price"] = trades.close_price.astype(float)

        strategy_type = list(trades.strategy_type.unique())[0]
        if strategy_type == StrategyType.intraday:
            columns_to_drop = list(
                {"date", "open", "high", "low", "close"}.intersection(
                    set(list(trades.columns))
                )
            )
            if columns_to_drop:
                trades = trades.drop(columns=columns_to_drop)

            trades = pd.merge(
                trades,
                self.market_data[
                    ["tradingsymbol", "date_only", "date", "high", "low", "close"]
                ],
                how="left",
                left_on=["tradingsymbol", "date_only"],
                right_on=["tradingsymbol", "date_only"],
            )

            Backtesting.add_attributes(trades)
            trades = trades[
                (trades.date > trades.entry_time) & (trades.date <= trades.exit_time)
            ]

            trades.loc[:, "is_trade_closed"] = np.where(
                (trades.exit_time == trades.date), 1, 0
            )

            Backtesting.apply_stoploss(trades)
            Backtesting.custom_exit(trades)
            Backtesting.apply_trailing_stoploss(trades)
            Backtesting.apply_trade_squareoff(trades)

            trades = trades[trades.is_trade_closed == 1]

            trades = (
                trades.groupby(["tradingsymbol", "entry_time"]).head(1).reset_index()
            )
            trades.loc[:, "closing_timestamp"] = trades.date
        else:
            trades.loc[:, "closing_timestamp"] = trades.exit_time

        interval_minutes = int(TickInterval.get_interval_seconds(interval) / 60)
        trades.loc[:, "order_timestamp"] = trades.entry_time + timedelta(
            minutes=interval_minutes
        )
        trades.loc[:, "closing_timestamp"] = trades.closing_timestamp + timedelta(
            minutes=interval_minutes
        )
        trades.loc[:, "date"] = trades.original_date
        trades.loc[:, "exposure"] = trades.quantity * trades.entry_price

        fno_slippage = 0
        if "fno_slippage" in args:
            fno_slippage = args["fno_slippage"]

        cm_slippage = 0
        if "cm_slippage" in args:
            cm_slippage = args["cm_slippage"]

        response = StrategyReport.generate_report(
            trades, fno_slippage=fno_slippage, cm_slippage=cm_slippage
        )
        result = pd.DataFrame(response)

        trades = StrategyReport.add_more_params(
            trades, fno_slippage=fno_slippage, cm_slippage=cm_slippage
        )

        StrategyReport.print_report(result)
        if "display_visuals" in args and args["display_visuals"] == False:
            Constants.logger.info("Skipping report display")
        else:
            StrategyReport.print_portfolio(trades, tag)

        return result, trades

    @staticmethod
    def apply_trade_squareoff(trades):

        if "trade_squareoff" not in trades.columns:
            return

        print("Applying trade squareoff")

        trades.loc[:, "trade_squareoff_price"] = np.where(
            trades.transaction_type == "SELL",
            Constants.round_to_tick((1 - trades.trade_squareoff) * trades.entry_price),
            Constants.round_to_tick((1 + trades.trade_squareoff) * trades.entry_price),
        )

        trades.loc[:, "is_trade_closed"] = np.where(
            (
                (
                    (trades.transaction_type == "SELL")
                    & (trades.low <= trades.trade_squareoff_price)
                )
                | (
                    (trades.transaction_type == "BUY")
                    & (trades.high >= trades.trade_squareoff_price)
                )
            ),
            1,
            trades.is_trade_closed,
        )

        trades.loc[:, "close_price"] = np.where(
            (
                (
                    (trades.transaction_type == "SELL")
                    & (trades.low <= trades.trade_squareoff_price)
                )
                | (
                    (trades.transaction_type == "BUY")
                    & (trades.high >= trades.trade_squareoff_price)
                )
            ),
            trades.trade_squareoff_price,
            trades.close_price,
        )

    @staticmethod
    def apply_strategy_squareoff(trades):

        if "strategy_squareoff" not in trades.columns:
            return trades

        print("Applying strategy squareoff")

        trades.loc[:, "squareoff_profit"] = (
            trades.strategy_squareoff * trades.entry_price
        )
        trades.loc[:, "trade_profit"] = np.where(
            trades.transaction_type == "SELL",
            trades.entry_price - trades.close,
            trades.close - trades.entry_price,
        )

        trades_combined_profits = (
            trades.groupby(["date", "uuid"])["squareoff_profit", "trade_profit"]
            .sum()
            .reset_index()
        )

        trades = trades.drop(columns=["squareoff_profit", "trade_profit"])

        trades = pd.merge(
            trades,
            trades_combined_profits,
            how="left",
            left_on=["date", "uuid"],
            right_on=["date", "uuid"],
        )

        trades.loc[:, "is_trade_closed"] = np.where(
            trades.trade_profit >= trades.squareoff_profit,
            1,
            trades.is_trade_closed,
        )

        trades.loc[:, "close_price"] = np.where(
            trades.trade_profit >= trades.squareoff_profit,
            trades.close,
            trades.close_price,
        )

        return trades

    @staticmethod
    def apply_stoploss(trades):

        if "stoploss" not in trades.columns:
            return
        minimum_stoploss = trades.stoploss.min()
        if minimum_stoploss <= 0:
            raise Exception(
                f"Invalid stoploss entry [{minimum_stoploss}] found in the trades data"
            )
        print("Applying stoploss")

        trades.loc[:, "stoploss_price"] = np.where(
            trades.transaction_type == "SELL",
            Constants.round_to_tick(
                ((1 + trades.stoploss) * trades.entry_price).astype(float)
            ),
            Constants.round_to_tick(
                ((1 - trades.stoploss) * trades.entry_price).astype(float)
            ),
        )

        trades.loc[:, "is_trade_closed"] = np.where(
            (
                (
                    (trades.transaction_type == "SELL")
                    & (trades.high >= trades.stoploss_price)
                )
                | (
                    (trades.transaction_type == "BUY")
                    & (trades.low <= trades.stoploss_price)
                )
            ),
            1,
            trades.is_trade_closed,
        )
        trades.loc[:, "close_price"] = np.where(
            (
                (
                    (trades.transaction_type == "SELL")
                    & (trades.high >= trades.stoploss_price)
                )
                | (
                    (trades.transaction_type == "BUY")
                    & (trades.low <= trades.stoploss_price)
                )
            ),
            trades.stoploss_price,
            trades.close_price,
        )

    @staticmethod
    def apply_trailing_stoploss(trades):

        if "trailing_stoploss" not in trades.columns:
            return
        print("Applying trailing stoploss")

        trades.loc[:, "entry_sl_trigger_price"] = np.where(
            trades.transaction_type == "SELL",
            Constants.round_to_tick(
                (1 + trades.trailing_stoploss) * trades.entry_price
            ),
            Constants.round_to_tick(
                (1 - trades.trailing_stoploss) * trades.entry_price
            ),
        )
        trades.loc[:, "sl_trigger_price"] = np.where(
            trades.transaction_type == "SELL",
            Constants.round_to_tick((1 + trades.trailing_stoploss) * trades.close),
            Constants.round_to_tick((1 - trades.trailing_stoploss) * trades.close),
        )

        trades.loc[:, "sl_trigger_price"] = np.minimum(
            trades.sl_trigger_price, trades.entry_sl_trigger_price
        )

        trades.loc[:, "is_trade_closed"] = np.where(
            (
                (
                    (trades.transaction_type == "SELL")
                    & (trades.high >= trades.sl_trigger_price)
                )
                | (
                    (trades.transaction_type == "BUY")
                    & (trades.low <= trades.sl_trigger_price)
                )
            ),
            1,
            trades.is_trade_closed,
        )
        trades.loc[:, "close_price"] = np.where(
            (
                (
                    (trades.transaction_type == "SELL")
                    & (trades.high >= trades.sl_trigger_price)
                )
                | (
                    (trades.transaction_type == "BUY")
                    & (trades.low <= trades.sl_trigger_price)
                )
            ),
            trades.sl_trigger_price,
            trades.close_price,
        )

    @staticmethod
    def custom_exit(trades):

        if "custom_exit" not in trades.columns:
            return

        print("Applying custom exit")

        assert len(trades.transaction_type.unique()) == 1
        assert trades.transaction_type.unique()[0] == "SELL"

        trades.loc[:, "is_trade_closed"] = np.where(
            trades.close >= trades.sma_9, 1, trades.is_trade_closed
        )
        trades.loc[:, "close_price"] = trades.close

    @staticmethod
    def add_attributes(trades):

        if "custom_exit" not in trades.columns:
            return

        trades.loc[:, "sma_9"] = trades.close.rolling(9).mean()
