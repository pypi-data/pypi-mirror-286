import re
import numpy as np
import uuid
from quantplay.utils.constant import Constants, OrderType, IntervalAttribute
from quantplay.service import market, backtesting
from quantplay.utils.exchange import Market as MarketConstants
from quantplay.model.exchange.order import QuantplayExchangeOrder
from quantplay.exception.exceptions import StrategyInvocationException
import datetime
import pandas as pd
import polars as pl
from datetime import timedelta

pd.options.mode.chained_assignment = None  # default='warn'


class QuantplayAlgorithm:
    MAX_LEN_FOR_STRATEGY_TAG = 15

    def __init__(self):
        self.add_derivative_symbols()

    def validate_production(self):
        if not hasattr(self, "strategy_trigger_times"):
            raise Exception("Strategy must have 'strategy_trigger_times' attribute")

        if not hasattr(self, "data_required_for_days"):
            raise Exception("Strategy must have 'data_required_for_days' attribute")

        if not hasattr(self, "execution_algo"):
            raise Exception("Strategy must have 'execution_algo' attribute")

        if not hasattr(self, "order_type"):
            raise Exception("Strategy must have 'order_type' attribute")

        supported_orders = [OrderType.market, OrderType.limit]
        if self.order_type not in supported_orders:
            raise Exception(
                "order type {} not supported, please use {}".format(
                    self.order_type, supported_orders
                )
            )
        self.validate()

    def validate(self):
        if not hasattr(self, "interval"):
            raise Exception("Strategy must have an 'interval' attribute.")

        if not hasattr(self, "exchange_to_trade_on"):
            raise Exception("Strategy must have an 'exchange_to_trade_on' attribute.")

        if not hasattr(self, "stream_symbols_by_security_type"):
            raise Exception(
                "Strategy must have an 'stream_symbols' dictionary attribute mapping exchange to symbol list"
            )

        if not hasattr(self, "strategy_type"):
            raise Exception(
                "Strategy must have 'strategy_type' attribute which can be either 'intraday' or 'overnight'"
            )

        if not hasattr(self, "entry_time"):
            raise Exception("Strategy must have 'entry_time' attribute")

        if not hasattr(self, "strategy_tag"):
            raise Exception("Strategy must have 'strategy_tag' attribute")
        else:
            if not self.strategy_tag.isalnum():
                raise Exception(
                    "strategy tag {} is not alphanumeric".format(self.strategy_tag)
                )
            if len(self.strategy_tag) > QuantplayAlgorithm.MAX_LEN_FOR_STRATEGY_TAG:
                raise Exception(
                    "length of strategy tag {} must have less than {} characters".format(
                        self.strategy_tag,
                        QuantplayAlgorithm.MAX_LEN_FOR_STRATEGY_TAG,
                    )
                )

        print("Strategy with tag {} successfully validated".format(self.strategy_tag))

    def should_exit(self, tick_time):
        tick_time_str = tick_time.strftime(Constants.hour_min_format)
        x = re.search(self.exit_time, tick_time_str)
        if x:
            return True
        return False

    def should_invoke(self, interval, tick_time):

        if interval != self.interval:
            return False

        tick_time_str = tick_time.strftime(Constants.hour_min_format)

        for trigger_time in self.strategy_trigger_times:
            x = re.search(trigger_time, tick_time_str)
            if x:
                return True
        return False

    def required_tick_interval(self):
        return self.interval

    def get_trades(self, market_data):
        """Implement in Strategy subclasses."""
        raise NotImplementedError("get_trades must be implemented")

    def add_orders_uuid(self, trades, columns=["date", "symbol"]):
        """Adds uuid column in trades after grouping by given columns.

        :param: columns: List[str], for each group of given columns, one single uuid will be attached
        """
        g = trades.groupby(columns)

        # number of unique class
        ngroups = g.ngroups

        # generate the uuid
        uuids = np.array([str(uuid.uuid4()) for _ in range(ngroups)])

        # map the group number to uuid
        trades["uuid"] = uuids[g.ngroup()]

    def filter_uuids_not_matching_count(self, trades):
        """Filters out trades with uuids not matching the self.exact_number_of_order_per_uuid count"""
        self.add_orders_uuid(trades, self.columns_for_uuid)

        trades.loc[
            :, "exact_number_of_orders_per_uuid"
        ] = self.exact_number_of_orders_per_uuid

        return trades[
            trades["uuid"].map(trades["uuid"].value_counts())
            == trades["exact_number_of_orders_per_uuid"]
        ]

    def live_orders(self, market_data, tick_time):
        """Returns list of QuantplayExchangeOrder tuples
        which are to be executed immediately.
        """
        try:
            trades = self.get_trades(market_data)

            if len(trades) == 0:
                return {"entry_orders": trades}

            interval_minutes = int(
                Constants.interval_attributes[self.interval][IntervalAttribute.seconds]
                / 60
            )

            trades.loc[:, "tag"] = self.strategy_tag
            trades.loc[:, "strategy_type"] = self.strategy_type
            trades.loc[:, "order_timestamp"] = trades.date.apply(
                lambda x: x + timedelta(minutes=interval_minutes)
            )

            exit_orders = []
            if "exit_time" in trades.columns:
                exit_trades = trades[trades.exit_time == tick_time]
                exit_trades = exit_trades.to_dict("records")
                exit_orders = QuantplayExchangeOrder.get_exchange_orders(
                    exit_trades,
                    order_type=self.order_type,
                    exchange=self.exchange_to_trade_on,
                    execution_algo=self.execution_algo,
                )

            entry_trades = trades[trades.date == tick_time]
            entry_trades = entry_trades.to_dict("records")
            entry_orders = QuantplayExchangeOrder.get_exchange_orders(
                entry_trades,
                order_type=self.order_type,
                exchange=self.exchange_to_trade_on,
                execution_algo=self.execution_algo,
            )

            return {"entry_orders": entry_orders, "exit_orders": exit_orders}
        except Exception as e:
            raise StrategyInvocationException(
                f"Failed to invoke strategy {self.strategy_tag}"
            ) from e

    def get_nearest_expiry_data(
        self, symbols, days_offset, after_date, before_date
    ) -> pl.DataFrame:
        expiry_data = pl.read_parquet(
            f"{market.nse_market_data_path}expiry_data.parquet"
        )

        expiry_data = expiry_data.filter(
            pl.col("expiry_date") >= pl.col("date").add(timedelta(days=days_offset))
        )
        expiry_data = expiry_data.filter(pl.col("symbol").is_in(symbols))
        expiry_data = (
            expiry_data.sort("expiry_date")
            .group_by(["symbol", "date"])
            .first()
            .sort("date")
        )
        if after_date is not None:
            expiry_data = expiry_data.filter(
                pl.col("date").dt.date().cast(pl.String) >= after_date
            )
        if before_date is not None:
            expiry_data = expiry_data.filter(
                pl.col("date").dt.date().cast(pl.String) <= before_date
            )

        return expiry_data

    def add_derivative_symbols(self, mode="backtest"):
        opt_derivative_symbols, fut_derivative_symbols = set(), set()

        equity_symbols = []
        if "EQ" in self.stream_symbols_by_security_type:
            equity_symbols = [
                MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP.get(
                    symbol, symbol
                )
                for symbol in self.stream_symbols_by_security_type["EQ"]
            ]

        if hasattr(self, "option_nearest_expiry_offset"):
            depth = None
            after_date = None
            before_date = None
            if hasattr(self, "option_chain_depth"):
                depth = self.option_chain_depth
            if hasattr(self, "backtest_after_date"):
                after_date = self.backtest_after_date
            if hasattr(self, "backtest_before_date"):
                before_date = self.backtest_before_date
            if mode == "prod":
                after_date = str(datetime.datetime.now().date())
                before_date = str(datetime.datetime.now().date())

            self.opt_expiry_data = self.get_nearest_expiry_data(
                symbols=equity_symbols,
                days_offset=self.option_nearest_expiry_offset,
                after_date=after_date,
                before_date=before_date,
            )
            opt_expiry_data_records = self.opt_expiry_data.to_dicts()
            for record in opt_expiry_data_records:
                (symbol, expiry_date, strike_gap, lowest_strike, highest_strike,) = (
                    record["symbol"],
                    record["expiry_date"],
                    int(record["strike_gap"]),
                    int(record["lowest_strike_price"]),
                    int(record["highest_strike_price"]),
                )
                formatted_expiry_date = market.format_expiry_date(
                    expiry_date, security_type="OPT"
                )
                ce_symbols = [
                    symbol + formatted_expiry_date + str(strike) + "CE"
                    for strike in range(lowest_strike, highest_strike, strike_gap)
                ]
                pe_symbols = [
                    symbol + formatted_expiry_date + str(strike) + "PE"
                    for strike in range(lowest_strike, highest_strike, strike_gap)
                ]
                opt_derivative_symbols.update(ce_symbols + pe_symbols)

            self.stream_symbols_by_security_type["OPT"] = list(opt_derivative_symbols)

        if hasattr(self, "future_nearest_expiry_offset"):
            self.fut_expiry_data = market.get_nearest_expiry_data(
                symbols=equity_symbols,
                days_offset=self.future_nearest_expiry_offset,
                security_type="FUT",
            )

            fut_expiry_data_records = self.fut_expiry_data.to_dict("records")
            for record in fut_expiry_data_records:
                symbol, expiry_date = record["symbol"], record["expiry_date"]
                expiry_date = datetime.date.fromisoformat(expiry_date)
                formatted_expiry_date = market.format_expiry_date(
                    expiry_date, security_type="FUT"
                )
                fut_derivative_symbols.add(symbol + formatted_expiry_date + "FUT")

            self.stream_symbols_by_security_type["FUT"] = list(fut_derivative_symbols)

    def add_expiry(self, trades, security_type=None):
        if security_type == "OPT":
            return market.add_expiry(
                trades,
                security_type=security_type,
                days_offset=self.option_nearest_expiry_offset,
            )

        if security_type == "FUT":
            return market.add_expiry(
                trades,
                security_type=security_type,
                days_offset=self.future_nearest_expiry_offset,
            )

    def backtest(self, **kwargs):
        if hasattr(self, "backtest_after_date"):
            kwargs["after"] = self.backtest_after_date
        if hasattr(self, "backtest_before_date"):
            kwargs["before"] = self.backtest_before_date
        market_data = market.data(
            symbols_by_security_type=self.stream_symbols_by_security_type,
            interval=self.interval,
            **kwargs,
        )
        trades = self.get_trades(market_data)
        print("Got {} trades from strategy".format(len(trades)))
        del market_data
        trades.loc[:, "tag"] = self.strategy_tag
        trades.loc[:, "strategy_type"] = self.strategy_type
        trades.loc[:, "entry_time"] = trades.date
        trades.loc[:, "exchange"] = self.exchange_to_trade_on

        holding_days = 0 if (self.strategy_type == "intraday") else self.holding_days

        backtesting.validate_trades(
            trades, columns_to_validate=["transaction_type", "strategy_type", "tag"]
        )

        security_types = list(trades.security_type.unique())
        symbols_by_security_type = {}
        for security_type in security_types:
            symbols_by_security_type[security_type] = list(
                trades[trades.security_type == security_type].tradingsymbol.unique()
            )

        trades.loc[:, "date_only"] = pd.to_datetime(trades.date.dt.date)

        backtesting.load_data(symbols_by_security_type, self.interval, **kwargs)
        if hasattr(self, "exit_time"):
            trades = backtesting.add_time(
                trades,
                column_time_tuple=("exit_time", self.exit_time),
                holding_days=holding_days,
            )
        backtesting.validate_trades(trades, columns_to_validate=["exit_time"])

        results, trades_res = backtesting.evaluate_performance(
            trades, self.interval, tag=self.strategy_tag, args=kwargs
        )

        return results, trades_res
