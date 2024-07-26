from quantplay.utils.data_utils import DataUtils
import requests
import json
from quantplay.utils.config_util import QuantplayConfig
import pandas as pd
import numpy as np
from quantplay.exception.exceptions import AccessDeniedException
from quantplay.utils.exchange import Market as MarketConstants
import copy
from datetime import timedelta
from os.path import expanduser
import re
from quantplay.broker.zerodha import Zerodha
from quantplay.broker.angelone import AngelOne
from quantplay.broker.motilal import Motilal
from quantplay.utils.constant import Constants
from datetime import datetime


class Market:
    BASE_URL = "https://7tpcay1yyk.execute-api.ap-south-1.amazonaws.com/prod/"

    GET_SYMBOLS_URL = "{}get_symbols".format(BASE_URL)
    EXPIRY_DATA_URL = "{}nearest_expiry".format(BASE_URL)
    SECURITY_DATA_URL = "{}get_security_delivery".format(BASE_URL)

    def __init__(self):
        config = QuantplayConfig.get_config()
        self.base_path = "{}/.quantplay/".format(expanduser("~"))
        self.nse_equity_path = "{}/.quantplay/NSE_EQ/".format(expanduser("~"))
        self.nse_opt_path = "{}/.quantplay/NSE_OPT/".format(expanduser("~"))
        self.nse_fut_path = "{}/.quantplay/NSE_FUT/".format(expanduser("~"))
        self.nse_market_data_path = "{}/.quantplay/NSE_MARKET_DATA/".format(
            expanduser("~")
        )
        self.mcx_path = "{}/.quantplay/MCX/".format(expanduser("~"))

        if "DEFAULT" in config and "base_path" in config["DEFAULT"]:
            self.base_path = config["DEFAULT"]["base_path"]
        if "DEFAULT" in config and "nse_equity_path" in config["DEFAULT"]:
            self.nse_equity_path = config["DEFAULT"]["nse_equity_path"]
        if "DEFAULT" in config and "nse_opt_path" in config["DEFAULT"]:
            self.nse_opt_path = config["DEFAULT"]["nse_opt_path"]
        if "DEFAULT" in config and "nse_fut_path" in config["DEFAULT"]:
            self.nse_fut_path = config["DEFAULT"]["nse_fut_path"]
        if "DEFAULT" in config and "nse_market_data_path" in config["DEFAULT"]:
            self.nse_market_data_path = config["DEFAULT"]["nse_market_data_path"]
        if "DEFAULT" in config and "mcx_path" in config["DEFAULT"]:
            self.mcx_path = config["DEFAULT"]["mcx_path"]

    def initialize_broker(self, broker_name=None):
        config = QuantplayConfig.get_config()

        if (
            "DEFAULT" in config
            and "preferred_broker" in config["DEFAULT"]
            and broker_name is None
        ):
            preferred_broker = config["DEFAULT"]["preferred_broker"]
            Constants.logger.info(
                "Using {} as preferred broker".format(preferred_broker)
            )
            broker_name = preferred_broker

        if broker_name is None:
            raise Exception("please provide broker_name to initialize broker")

        if broker_name == "Zerodha":
            self.broker = Zerodha(wrapper=config["DEFAULT"]["zerodha_wrapper"])
        elif broker_name == "AngelOne":
            self.broker = AngelOne()
        elif broker_name == "Motilal":
            self.broker = Motilal()
        else:
            raise Exception("broker [{}] not supported".format(broker_name))

    def symbols(self, universe=None, filters={}):
        credentials = QuantplayConfig.get_credentials()
        if "DEFAULT" not in credentials or "access_token" not in credentials["DEFAULT"]:
            raise AccessDeniedException(
                "Access Denied, please signin using [quantplay user signin]"
            )
        input = {}
        if universe != None:
            input["universe"] = universe

        access_token = credentials["DEFAULT"]["access_token"]
        input["access_token"] = access_token
        input["filters"] = filters

        x = requests.post(Market.GET_SYMBOLS_URL, data=json.dumps(input))
        response = json.loads(x.text)

        if "error" in response and response["error"] == True:
            print(response["message"])
            raise Exception(response["message"])

        return response["data"]

    def add_security_delivery_data(self, trades):
        credentials = QuantplayConfig.get_credentials()
        if "DEFAULT" not in credentials or "access_token" not in credentials["DEFAULT"]:
            raise AccessDeniedException(
                "Access Denied, please signin using [quantplay user signin]"
            )

        access_token = credentials["DEFAULT"]["access_token"]

        data = copy.deepcopy(trades[["symbol", "date"]])
        data.loc[:, "date"] = trades.date.dt.date.astype(str)

        request_input = {}
        request_input["access_token"] = access_token
        request_input["data"] = data.to_dict("records")

        x = requests.post(Market.SECURITY_DATA_URL, data=json.dumps(request_input))

        response = json.loads(x.text)
        df = pd.DataFrame(response["data"])
        trades.loc[:, "yesterdays_delivery_ratio"] = df.yesterdays_delivery_ratio
        trades.loc[:, "delivery_ratio"] = df.delivery_ratio

    def future_symbol(self, trade_data):
        trades = copy.deepcopy(trade_data)
        trades.loc[:, "tradingsymbol"] = trades["symbol"].replace(
            MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP
        )

        trades.loc[:, "tradingsymbol"] = trades.tradingsymbol + trades[
            "expiry_date"
        ].dt.strftime("%y").astype(str)

        trades.loc[:, "tradingsymbol"] = (
            trades.tradingsymbol + trades["expiry_date"].dt.strftime("%b").str.upper()
        )

        trades.loc[:, "tradingsymbol"] = trades.tradingsymbol + "FUT"
        trades.loc[:, "security_type"] = "FUT"

        return trades

    def option_symbol(self, trade_data, price_column=None, option_type=None):
        trades = copy.deepcopy(trade_data)

        trades.loc[:, "tradingsymbol"] = trades["symbol"].replace(
            MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP
        )
        trades.loc[:, "tradingsymbol"] = trades.tradingsymbol + trades[
            "expiry_date"
        ].dt.strftime("%y").astype(str)

        trades.loc[:, "month_number"] = (
            trades["expiry_date"].dt.strftime("%m").astype(int).astype(str)
        )
        trades.loc[:, "monthly_option_prefix"] = (
            trades["expiry_date"].dt.strftime("%b").str.upper()
        )

        trades.loc[:, "week_option_prefix"] = np.where(
            trades.month_number.astype(int) >= 10,
            trades.monthly_option_prefix.str[0]
            + trades["expiry_date"].dt.strftime("%d").astype(str),
            trades.month_number + trades["expiry_date"].dt.strftime("%d").astype(str),
        )

        trades.loc[:, "next_expiry"] = trades.expiry_date + pd.DateOffset(days=7)

        trades.loc[:, "tradingsymbol"] = np.where(
            trades.expiry_date.dt.month != trades.next_expiry.dt.month,
            trades.tradingsymbol + trades.monthly_option_prefix,
            trades.tradingsymbol + trades.week_option_prefix,
        )

        trades.loc[:, "tradingsymbol"] = trades.tradingsymbol + trades[
            price_column
        ].astype(str)
        if option_type is not None:
            trades.loc[:, "tradingsymbol"] = trades.tradingsymbol + option_type
        else:
            trades.loc[:, "tradingsymbol"] = trades.tradingsymbol + trades.option_type

        trades.loc[:, "security_type"] = "OPT"

        trades = trades.drop(
            [
                "next_expiry",
                "week_option_prefix",
                "monthly_option_prefix",
                "month_number",
            ],
            axis=1,
        )
        return trades

    @staticmethod
    def filter_contracts_matching_expiry_date(option_data):
        if "expiry_date" not in option_data.columns:
            raise Exception("expiry_date column required in option_data")

        if "symbol" not in option_data.columns:
            raise Exception("symbol column required in option_data")

        return option_data[
            option_data.apply(
                lambda x: x["symbol"].startswith(
                    MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP[
                        x["equity_symbol"]
                    ]
                    + Market.format_expiry_date(x["expiry_date"], "OPT")
                ),
                axis=1,
            )
        ]

    @staticmethod
    def add_columns_in_option_data(option_data, columns=[]):
        def get_strike_price(x):
            try:
                return int(
                    x["symbol"].split(
                        MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP[
                            x["equity_symbol"]
                        ]
                        + Market.format_expiry_date(x["expiry_date"], "OPT")
                    )[1][:-2]
                )
            except Exception as e:
                print(x)
                raise e

        columns_supported = ["equity_symbol", "strike_price", "option_type"]
        if not set(columns).issubset(columns_supported):
            raise Exception(
                f"supports only addition of columns {columns_supported}, but received {columns}"
            )

        for col in columns:
            if col == "equity_symbol":
                option_data.loc[:, "equity_symbol"] = option_data.symbol.apply(
                    lambda x: MarketConstants.DERIVATIVE_SYMBOL_TO_INDEX_SYMBOL_MAP[
                        re.findall("([a-zA-Z]*)\d*.*", x)[0]
                    ]
                )
            elif col == "strike_price":
                option_data.loc[:, "strike_price"] = option_data[
                    ["date", "expiry_date", "symbol", "equity_symbol"]
                ].apply(
                    lambda x: get_strike_price(x),
                    axis=1,
                )

            elif col == "option_type":
                option_data.loc[:, "option_type"] = option_data.symbol.apply(
                    lambda x: x[-2:]
                )

    @staticmethod
    def format_expiry_date(expiry_date, security_type):
        formatted_date = expiry_date.strftime("%y")
        month_number, month_name, day = (
            expiry_date.month,
            expiry_date.strftime("%b").upper(),
            expiry_date.strftime("%d"),
        )

        if security_type == "FUT":
            formatted_date += month_name
        elif security_type == "OPT":
            if month_number >= 10:
                week_prefix = month_name[0] + day
            else:
                week_prefix = str(month_number) + day

            next_expiry = expiry_date + timedelta(days=7)
            if next_expiry.month == expiry_date.month:
                formatted_date += week_prefix
            else:
                formatted_date += month_name
        else:
            raise Exception(
                "Invalid security_type {}. Date argument was {}".format(
                    security_type, expiry_date
                )
            )

        return formatted_date

    def equity_data(self, interval=None, symbols=None):
        df = DataUtils.load_data_using_pandas(
            stocks=symbols, interval=interval, path=self.nse_equity_path
        )
        df.loc[:, "security_type"] = "EQ"
        return df

    def data_by_path(self, interval=None, symbols=None, path=None):
        df = DataUtils.load_data_using_pandas(
            stocks=symbols, interval=interval, path=path
        )

        return df

    def mcx_data(self, interval=None, symbols=None):
        df = DataUtils.load_data_using_pandas(
            stocks=symbols, interval=interval, path=self.mcx_path
        )
        return df

    def data(self, interval=None, symbols_by_security_type=None, **kwargs):
        security_type_data_path = {
            "EQ": self.nse_equity_path,
            "FUT": self.nse_fut_path,
            "OPT": self.nse_opt_path,
        }
        if "path_suffix" in kwargs:
            for key in security_type_data_path:
                security_type_data_path[key] = (
                    security_type_data_path[key] + kwargs["path_suffix"]
                )

        dfs = []
        for security_type, symbols in symbols_by_security_type.items():

            print(
                f"Loading {security_type} data for {len(set(symbols))} symbols, interval {interval}"
            )
            df = DataUtils.load_data_using_pandas(
                stocks=symbols,
                interval=interval,
                path=security_type_data_path[security_type],
                ignore_if_not_found=True,
                **kwargs,
            )
            df.loc[:, "security_type"] = security_type
            dfs.append(df)

        return pd.concat(dfs, axis=0)

    def options_data(self, interval=None, symbols=None):
        df = DataUtils.load_data_using_pandas(
            stocks=symbols, interval=interval, path=self.nse_opt_path
        )
        df.loc[:, "security_type"] = "OPT"
        return df

    def future_data(self, interval=None, symbols=None):
        df = DataUtils.load_data_using_pandas(
            stocks=symbols, interval=interval, path=self.nse_fut_path
        )
        df.loc[:, "security_type"] = "FUT"
        return df

    def get_trades(self, data, entry_time):
        return data[
            data.assign(Time=data["date"].dt.time.astype(str))["Time"].str.match(
                entry_time
            )
        ]

    @staticmethod
    def merge_price(
        trades,
        data,
        time=None,
        column_name=None,
        merge_on_columns=["symbol", "date_only"],
        column_type="close",
    ):
        filter_data = data[
            data.assign(Time=data["date"].dt.time.astype(str))["Time"].str.match(time)
        ]

        filter_data.loc[:, column_name] = filter_data[column_type]
        trades = pd.merge(
            trades,
            filter_data[[column_name] + merge_on_columns],
            how="left",
            left_on=merge_on_columns,
            right_on=merge_on_columns,
        )

        return trades

    @staticmethod
    def add_intraday_metrics(data, entry_time, exit_time):
        data.loc[:, "intraday_high"] = data.high
        data.loc[:, "intraday_low"] = data.low

        condition = (data.date.dt.time <= pd.to_datetime(entry_time).time()) | (
            data.date.dt.time > pd.to_datetime(exit_time).time()
        )
        data.loc[:, "intraday_high"] = np.where(condition, np.nan, data.intraday_high)
        data.loc[:, "intraday_low"] = np.where(condition, np.nan, data.intraday_low)

        data.loc[:, "date_only"] = data.date.dt.date
        data.loc[:, "intraday_high"] = data.groupby(
            ["symbol", "date_only"]
        ).intraday_high.transform(max)
        data.loc[:, "intraday_low"] = data.groupby(
            ["symbol", "date_only"]
        ).intraday_low.transform(min)

    def day_candle(self, market_data):
        day_candle = (
            market_data.groupby(["symbol", pd.Grouper(key="date", freq="1d")])
            .agg(
                {
                    "open": "first",
                    "high": "max",
                    "low": "min",
                    "close": "last",
                    "volume": "sum",
                }
            )
            .reset_index()
        )

        return day_candle
