import traceback
import json

import pandas as pd
import numpy as np
import pickle
import codecs
from datetime import datetime

from quantplay.broker.generics.broker import Broker
from quantplay.utils.constant import Constants, timeit, OrderType
from quantplay.broker.xts_utils.Connect import XTSConnect
from quantplay.utils.pickle_utils import PickleUtils, InstrumentData
from quantplay.exception.exceptions import (
    InvalidArgumentException,
    RetryableException,
    retry_exception,
)
from quantplay.broker.xts_utils.InteractiveSocketClient import OrderSocket_io

from quantplay.exception.exceptions import TokenException
import requests, time
from retrying import retry
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class XTS(Broker):
    source = "WebAPI"

    @timeit(MetricName="XTS:__init__")
    def __init__(
        self,
        api_key=None,
        api_secret=None,
        md_api_key=None,
        md_api_secret=None,
        order_updates=None,
        wrapper=None,
        md_wrapper=None,
        ClientID=None,
        load_instrument=True,
    ):
        super(XTS, self).__init__()
        self.order_updates = order_updates

        try:
            if wrapper:
                self.set_wrapper(wrapper, md_wrapper)
                self.ClientID = ClientID
                self.wrapper.root = self.root_url
                self.md_wrapper.root = self.root_url
            else:
                self.login(api_key, api_secret, md_api_key, md_api_secret)
        except Exception as e:
            print(traceback.print_exc())
            raise e

        if load_instrument:
            self.load_instrument()

    def set_wrapper(self, serialized_wrapper, serialized_md_wrapper):
        self.wrapper = pickle.loads(
            codecs.decode(serialized_wrapper.encode(), "base64")
        )
        self.md_wrapper = pickle.loads(
            codecs.decode(serialized_md_wrapper.encode(), "base64")
        )

    def load_instrument(self):
        # TODO: Check for Futures
        try:
            self.symbol_data = InstrumentData.get_instance().load_data(
                "xts_instruments"
            )
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from cache")
        except Exception as e:
            instruments = pd.read_csv(
                "https://quantplay-public-data.s3.ap-south-1.amazonaws.com/symbol_data/instruments.csv"
            )
            instruments = instruments.to_dict("records")
            self.symbol_data = {}

            for instrument in instruments:
                exchange = instrument["exchange"]
                tradingsymbol = instrument["tradingsymbol"]
                # NIFTY 08JUN2023 PE 17850 <- NIFTY2360817850PE
                # 2023-06-27 -> 08JUN2023
                # For FUTURES : EURINR23AUGFUT -> EURINR 23AUG2023 FUT

                ins_type = instrument["instrument_type"]
                name = instrument["name"]
                if ins_type in ["CE", "PE"]:
                    expiry = datetime.strftime(
                        datetime.strptime(str(instrument["expiry"]), "%Y-%m-%d"),
                        "%d%b%Y",
                    ).upper()
                    strike = str(instrument["strike"]).rstrip("0")
                    if strike[-1] == ".":
                        strike = strike[:-1]
                    instrument["broker_symbol"] = f"{name} {expiry} {ins_type} {strike}"
                elif ins_type == "FUT":
                    expiry = datetime.strftime(
                        datetime.strptime(str(instrument["expiry"]), "%Y-%m-%d"),
                        "%d%b%Y",
                    ).upper()
                    instrument["broker_symbol"] = f"{name} {expiry}"
                else:
                    instrument["broker_symbol"] = tradingsymbol

                self.symbol_data["{}:{}".format(exchange, tradingsymbol)] = instrument

            PickleUtils.save_data(self.symbol_data, "xts_instruments")
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from server")
        self.initialize_broker_symbol_map()

    def login(self, api_key, api_secret, md_api_key, md_api_secret):
        try:
            self.wrapper = XTSConnect(
                apiKey=api_key,
                secretKey=api_secret,
                root=self.root_url,
            )
            xt_core_response = self.wrapper.interactive_login()
            self.md_wrapper = XTSConnect(
                apiKey=md_api_key,
                secretKey=md_api_secret,
                root=self.root_url,
            )
            md_response = self.md_wrapper.marketdata_login()
            if "type" not in xt_core_response or xt_core_response["type"] != "success":
                print(f"api login response {xt_core_response}")
                raise TokenException("Api key credentials are incorrect")
            if "type" not in md_response or md_response["type"] != "success":
                print(f"market data login response {md_response}")
                raise TokenException("Market data api credentials are invalid")
            self.ClientID = xt_core_response["result"]["userID"]
        except TokenException as e:
            raise
        except Exception as e:
            raise InvalidArgumentException("Invalid api key/secret")

    def handle_exception(self, response):
        if "data" in response and "description" in response["data"]:
            data = response["data"]
            if "max limit" in data["description"].lower():
                user_id = self.profile()["user_id"]
                print("Rate limit problem")
                raise RetryableException(f"{user_id}: Request limit exceeded")
        if (
            "description" in response
            and "Authorization not found" in response["description"]
        ):
            raise TokenException(response["description"])
        if "type" in response and response["type"] == "error":
            raise Exception("[XTS_Error]: " + response["description"])

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def margins(self) -> dict:
        # TODO: Edit For Dealers

        api_response = self.wrapper.get_balance(clientID=self.ClientID)
        self.handle_exception(api_response)

        if not api_response:
            return {
                "margin_used": 0,
                "margin_available": 0,
            }
        api_response = api_response["result"]["BalanceList"][0]["limitObject"]
        return {
            # TODO: Get PNL
            "pnl": 0,
            "margin_used": api_response["RMSSubLimits"]["marginUtilized"],
            "margin_available": api_response["RMSSubLimits"]["netMarginAvailable"],
        }

    def account_summary(self):
        # TODO: Edit For Dealers
        margins = self.margins()
        margins["pnl"] = float(self.positions().pnl.sum())
        return margins

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def profile(self):
        api_response = self.wrapper.get_profile(self.ClientID)
        self.handle_exception(api_response)
        api_response = api_response["result"]

        response = {
            "user_id": api_response["ClientId"],
            "full_name": api_response["ClientName"],
            "segments": api_response["ClientExchangeDetailsList"],
        }

        return response

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def orders(self, tag=None, order_type=None, add_ltp=True):
        api_response = self.wrapper.get_order_book(self.ClientID)
        self.handle_exception(api_response)

        api_response = api_response["result"]

        orders = pd.DataFrame(api_response)
        positions = self.positions()
        positions = positions.sort_values("product").groupby(["tradingsymbol"]).head(1)
        if orders is None or len(orders) == 0:
            return pd.DataFrame(columns=self.orders_column_list)

        orders.loc[:, "tradingsymbol"] = orders.TradingSymbol
        orders = pd.merge(
            orders,
            positions[["tradingsymbol", "ltp"]],
            how="left",
            left_on=["tradingsymbol"],
            right_on=["tradingsymbol"],
        )

        orders.rename(
            columns={
                "ClientID": "user_id",
                "AppOrderID": "order_id",
                "OrderStatus": "status",
                "ExchangeSegment": "exchange",
                "OrderPrice": "price",
                "OrderType": "order_type",
                "OrderSide": "transaction_type",
                "OrderAverageTradedPrice": "average_price",
                "OrderGeneratedDateTime": "order_timestamp",
                "OrderQuantity": "quantity",
                "CumulativeQuantity": "filled_quantity",
                "LeavesQuantity": "pending_quantity",
                "ProductType": "product",
                "OrderStopPrice": "trigger_price",
                "OrderUniqueIdentifier": "tag",
                "ExchangeInstrumentID": "token",
                "OrderCategoryType": "variety",
            },
            inplace=True,
        )

        orders.loc[:, "filled_quantity"] = orders.filled_quantity.astype(float)
        orders.loc[:, "average_price"] = np.where(
            orders.average_price == "", 0, orders.average_price
        )
        orders.loc[:, "average_price"] = orders.average_price.astype(float)
        orders["order_id"] = orders["order_id"].astype(str)

        orders.loc[:, "pnl"] = (
            orders.ltp * orders.filled_quantity
            - orders.average_price * orders.filled_quantity
        )
        orders.loc[:, "pnl"] = np.where(
            orders.transaction_type == "SELL", -orders.pnl, orders.pnl
        )
        orders.loc[:, "order_timestamp"] = pd.to_datetime(
            orders.order_timestamp, format="%d-%m-%Y %H:%M:%S"
        )
        orders.loc[:, "update_timestamp"] = pd.to_datetime(
            orders.LastUpdateDateTime, format="%d-%m-%Y %H:%M:%S"
        )

        orders.loc[:, "exchange"] = orders.exchange.replace(
            ["NSECM", "NSEFO"], ["NSE", "NFO"]
        )
        orders.loc[:, "status"] = orders.status.replace(
            ["Rejected", "Cancelled", "Filled", "New"],
            ["REJECTED", "CANCELLED", "COMPLETE", "OPEN"],
        )
        orders.loc[:, "order_type"] = orders.order_type.replace(
            ["Limit", "StopLimit", "Market"], ["LIMIT", "SL", "MARKET"]
        )

        existing_columns = list(orders.columns)
        columns_to_keep = list(
            set(self.orders_column_list).intersection(set(existing_columns))
        )
        orders = orders[columns_to_keep]

        if tag:
            orders = orders[orders.tag == tag]

        if order_type:
            orders = orders[orders.order_type == order_type]

        return orders

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def positions(self):
        # TODO: get sell_value, buy_value
        api_response = self.wrapper.get_position_daywise(self.ClientID)
        self.handle_exception(api_response)

        api_response = api_response["result"]["positionList"]
        positions = pd.DataFrame(api_response)

        if len(positions) == 0:
            return pd.DataFrame(columns=self.positions_column_list)

        positions.rename(
            columns={
                "TradingSymbol": "tradingsymbol",
                "ExchangeSegment": "exchange",
                "OpenBuyQuantity": "buy_quantity",
                "OpenSellQuantity": "sell_quantity",
                "Quantity": "quantity",
                "SumOfTradedQuantityAndPriceBuy": "buy_value",
                "SumOfTradedQuantityAndPriceSell": "sell_value",
                "ProductType": "product",
                "ExchangeInstrumentId": "token",
            },
            inplace=True,
        )

        positions.loc[:, "exchange"] = positions.exchange.replace(
            ["NSECM", "NSEFO"], ["NSE", "NFO"]
        )

        positions.loc[:, "exchange_symbol"] = (
            positions["exchange"] + ":" + positions["token"]
        )

        symbols = positions.exchange_symbol.unique().tolist()
        symbol_ltps = self.get_ltps(symbols)

        positions.loc[:, "ltp"] = positions.token.apply(lambda x: symbol_ltps[int(x)])
        positions.loc[:, "pnl"] = positions.sell_value.astype(
            float
        ) - positions.buy_value.astype(float)
        positions.loc[:, "pnl"] += positions.quantity.astype(float) * positions.ltp
        positions.loc[:, "quantity"] = positions.quantity.astype(int)
        positions.loc[:, "buy_quantity"] = positions.buy_quantity.astype(int)
        positions.loc[:, "sell_quantity"] = positions.sell_quantity.astype(int)

        positions["tradingsymbol"] = positions.apply(
            lambda row: self.get_quantplay_symbol(row["tradingsymbol"]),
            axis=1,
        )
        positions.loc[:, "option_type"] = np.where(
            "PE" == positions.tradingsymbol.str[-2:], "PE", None
        )
        positions.loc[:, "option_type"] = np.where(
            "CE" == positions.tradingsymbol.str[-2:], "CE", positions.option_type
        )
        positions.loc[:, "option_type"] = np.where(
            positions.exchange.isin(["NFO", "BFO"]), positions.option_type, None
        )

        existing_columns = list(positions.columns)
        columns_to_keep = list(
            set(self.positions_column_list).intersection(set(existing_columns))
        )
        return positions[columns_to_keep]

    def get_quantplay_symbol(self, symbol):
        if symbol in self.broker_symbol_map:
            return self.broker_symbol_map[symbol]
        return symbol

    def get_ltps(self, symbols):
        instruments = [
            {
                "exchangeSegment": int(self.get_exchange_code(x.split(":")[0])),
                "exchangeInstrumentID": int(x.split(":")[1]),
            }
            for x in symbols
        ]
        api_response = self.md_wrapper.get_quote(
            Instruments=instruments,
            xtsMessageCode=1512,
            publishFormat="JSON",
        )

        if "type" in api_response and api_response["type"] == "error":
            raise TokenException(api_response["description"])
        api_response = api_response["result"]

        ltp_json = api_response["listQuotes"]

        ltp = [json.loads(x) for x in ltp_json]

        ltp = {x["ExchangeInstrumentID"]: x["LastTradedPrice"] for x in ltp}
        return ltp

    def get_exchange_code(self, exchange):
        exchange_code_map = {
            "NSE": 1,
            "NFO": 2,
            "BFO": 12,
            "BSE": 11,
            "NSECM": 1,
            "NSEFO": 2,
            "NSECD": 3,
            "BSECM": 11,
            "BSEFO": 12,
        }

        if exchange not in exchange_code_map:
            raise KeyError(
                f"INVALID_EXCHANGE: Exchange {exchange} not in ['NSE', 'NFO', 'NSECD', 'BSECM', 'BSEFO']"
            )

        return exchange_code_map[exchange]

    def get_exchange_name(self, exchange):
        exchange_code_map = {
            "NSE": "NSECM",
            "NFO": "NSEFO",
            "BFO": "BSEFO",
            "NSECD": "NSECD",
            "BSECM": "BSECM",
            "BSEFO": "BSEFO",
        }

        if exchange not in exchange_code_map:
            raise KeyError(
                f"INVALID_EXCHANGE: Exchange {exchange} not in ['NSE', 'NFO', 'NSECD', 'BSECM', 'BSEFO']"
            )

        return exchange_code_map[exchange]

    def get_ltp(self, exchange=None, tradingsymbol=None):
        exchange_code = self.get_exchange_code(exchange)
        exchange_token = self.symbol_data[f"{exchange}:{tradingsymbol}"][
            "exchange_token"
        ]

        api_response = self.md_wrapper.get_quote(
            Instruments=[
                {
                    "exchangeSegment": exchange_code,
                    "exchangeInstrumentID": exchange_token,
                }
            ],
            xtsMessageCode=1512,
            publishFormat="JSON",
        )["result"]

        ltp_json = api_response["listQuotes"][0]

        ltp = json.loads(ltp_json)["LastTradedPrice"]

        return ltp

    def place_order(
        self,
        tradingsymbol=None,
        exchange=None,
        quantity=None,
        order_type=None,
        transaction_type=None,
        tag=None,
        product=None,
        price=None,
        trigger_price: float = 0,
    ):
        exchange_name = self.get_exchange_name(exchange)
        order_type = self.get_order_type(order_type)

        exchange_token = self.symbol_data[f"{exchange}:{tradingsymbol}"][
            "exchange_token"
        ]
        if trigger_price is None:
            trigger_price = 0

        api_response = self.wrapper.place_order(
            exchangeSegment=exchange_name,
            exchangeInstrumentID=exchange_token,
            orderType=order_type,
            disclosedQuantity=0,
            orderQuantity=quantity,
            limitPrice=price,
            timeInForce="DAY",
            stopPrice=trigger_price,
            orderSide=transaction_type,
            productType=product,
            orderUniqueIdentifier=tag,
            clientID=self.ClientID,
        )
        Constants.logger.info(f"[XTS_PLACE_ORDER_RESPONSE] {api_response}")

        if api_response["type"] == "error":
            Constants.logger.info(f"[XTS_PLACE_ORDER_ERROR] {api_response}")

            raise Exception("[XTS_ERROR]: " + api_response["description"])

        return api_response["result"]["AppOrderID"]

    @timeit(MetricName="XTS:holdings")
    def holdings(self):
        return pd.DataFrame(columns=self.holdings_column_list)

    def cancel_order(self, order_id):
        orders = self.orders()

        order_data = orders[orders.order_id == str(order_id)]
        if len(order_data) == 0:
            raise InvalidArgumentException(f"Order [{order_id}] not found")
        order_data = order_data.to_dict("records")[0]

        tag = order_data["tag"]

        api_response = self.wrapper.cancel_order(
            appOrderID=int(order_id),
            clientID=order_data["user_id"],
            orderUniqueIdentifier=tag,
        )

        if api_response["type"] == "error":
            Constants.logger.info(f"[XTS_CANCEL_ORDER_ERROR] {api_response}")

            raise Exception("[XTS_ERROR]: " + api_response["description"])

        return api_response["result"]["AppOrderID"]

    def get_order_type(self, order_type):
        if order_type == OrderType.market:
            return "Market"
        elif order_type == OrderType.sl:
            return "StopLimit"
        elif order_type == OrderType.slm:
            return "StopMarket"
        elif order_type == OrderType.limit:
            return "Limit"

        return order_type

    def modify_order(self, data):
        order_id = data.get("order_id", None)
        price = data.get("price", None)
        trigger_price = data.get("trigger_price", None)
        order_type = data.get("order_type", None)
        tag = data.get("tag", None)
        product = data.get("product", None)

        orders = self.orders()
        order_data = orders[orders.order_id == order_id]
        if len(order_data) == 0:
            raise InvalidArgumentException(f"Order [{order_id}] not found")
        order_data = order_data.to_dict("records")[0]

        price = price or order_data["price"]
        trigger_price = trigger_price or order_data["trigger_price"]
        order_type = order_type or order_data["order_type"]
        tag = tag or order_data["tag"]
        product = product or order_data["product"]

        quantity = order_data["quantity"]
        time_in_force = "DAY"
        disclosed_quantity = 0

        api_response = self.wrapper.modify_order(
            appOrderID=order_id,
            modifiedTimeInForce=time_in_force,
            modifiedDisclosedQuantity=disclosed_quantity,
            modifiedLimitPrice=price,
            modifiedOrderQuantity=quantity,
            modifiedOrderType=self.get_order_type(order_type),
            modifiedProductType=product,
            modifiedStopPrice=trigger_price,
            orderUniqueIdentifier=tag,
            clientID=self.ClientID,
        )

        if api_response["type"] == "error":
            Constants.logger.info(f"[XTS_MODIFY_ORDER_ERROR] {api_response}")

            raise Exception("[XTS_ERROR]: " + api_response["description"])

        return api_response["result"]["AppOrderID"]

    def modify_price(self, order_id, price, trigger_price=None, order_type=None):
        return self.modify_order(
            {
                "order_id": str(order_id),
                "price": price,
                "trigger_price": trigger_price,
                "order_type": order_type,
            }
        )

    def stream_order_updates(self):
        socket = OrderSocket_io(
            userID=self.ClientID,
            token=self.wrapper.token,
            root_url=self.root_url,
        )
        socket.setup_event_listners(on_order=self.order_event_handler)
        socket.connect()

    def order_event_handler(self, order):
        order = json.loads(order)
        new_ord = {}

        try:
            new_ord["placed_by"] = order["ClientID"]
            new_ord["tag"] = order["ClientID"]
            new_ord["order_id"] = order["AppOrderID"]
            new_ord["exchange_order_id"] = order["ExchangeOrderID"]
            new_ord["exchange"] = order["ExchangeSegment"]
            new_ord["tradingsymbol"] = order["TradingSymbol"]

            if new_ord["exchange"] == "NSEFO":
                new_ord["exchange"] = "NFO"
            elif new_ord["exchange"] == "NSECM":
                new_ord["exchange"] = "NSE"

            if new_ord["exchange"] in ["NFO", "MCX"]:
                new_ord["tradingsymbol"] = self.broker_symbol_map[
                    new_ord["tradingsymbol"]
                ]

            new_ord["order_type"] = order["OrderType"].upper()
            new_ord["product"] = order["ProductType"].upper()
            new_ord["transaction_type"] = order["OrderSide"].upper()
            new_ord["quantity"] = int(order["OrderQuantity"])

            if "OrderStopPrice" in order:
                new_ord["trigger_price"] = float(order["OrderStopPrice"])
            else:
                new_ord["trigger_price"] = None

            new_ord["price"] = float(order["OrderPrice"])
            new_ord["status"] = order["OrderStatus"].upper()

            if new_ord["status"] == "PENDINGNEW":
                new_ord["status"] = "TRIGGER PENDING"
            elif new_ord["status"] == "PENDINGCANCEL":
                new_ord["status"] = "PENDING"
            elif new_ord["status"] == "PENDINGREPLACE":
                new_ord["status"] = "TRIGGER PENDING"
            elif new_ord["status"] == "REPLACED":
                new_ord["status"] = "UPDATE"
            elif new_ord["status"] == "NEW":
                new_ord["status"] = "OPEN"
            elif new_ord["status"] == "FILLED":
                new_ord["status"] = "COMPLETE"

            if new_ord["order_type"].upper() == "MARKET":
                new_ord["order_type"] = OrderType.market
            elif new_ord["order_type"].upper() == "STOPLIMIT":
                new_ord["order_type"] = OrderType.sl
            elif new_ord["order_type"].upper() == "STOPMARKET":
                new_ord["order_type"] = OrderType.slm
            elif new_ord["order_type"].upper() == "LIMIT":
                new_ord["order_type"] = OrderType.limit

            if new_ord["order_type"] == "LIMIT" and new_ord["status"] == "UPDATE":
                new_ord["status"] = "OPEN"

            if new_ord["status"] == "TRIGGER PENDING" and new_ord["trigger_price"] == 0:
                return
            self.order_updates.put(new_ord)

        except Exception as e:
            print(e)
            Constants.logger.error("[ORDER_UPDATE_PROCESSING_FAILED] {}".format(e))
