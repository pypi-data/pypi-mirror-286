import json
import traceback

import pandas as pd
import pyotp
from retrying import retry
from SmartApi import SmartConnect

import binascii
from quantplay.broker.generics.broker import Broker
from quantplay.exception.exceptions import InvalidArgumentException
from quantplay.model.broker.generics import ModifyOrderRequest
from quantplay.utils.exchange import Market as MarketConstants
from quantplay.exception.exceptions import (
    QuantplayOrderPlacementException,
    TokenException,
    ServiceException,
    RetryableException,
    retry_exception,
    BrokerException,
)
from requests.exceptions import ConnectTimeout, ConnectionError
import pickle
import codecs
from quantplay.wrapper.aws.s3 import S3Utils

from quantplay.utils.pickle_utils import InstrumentData

from quantplay.utils.constant import Constants, OrderType, timeit


class AngelOne(Broker):
    order_sl = "STOPLOSS_LIMIT"
    order_slm = "STOPLOSS_MARKET"

    @timeit(MetricName="Angelone:init")
    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=5,
        retry_on_exception=retry_exception,
    )
    def __init__(
        self,
        order_updates=None,
        api_key=None,
        user_id=None,
        mpin=None,
        totp=None,
        refresh_token=None,
        feed_token=None,
        access_token=None,
        load_instrument=True,
    ):
        super(AngelOne, self).__init__()
        self.order_updates = order_updates

        try:
            if refresh_token:
                self.wrapper = SmartConnect(
                    api_key=api_key,
                    access_token=access_token,
                    refresh_token=refresh_token,
                    feed_token=feed_token,
                )
                self.refresh_token = refresh_token
            else:
                self.wrapper = SmartConnect(api_key=api_key)
                response = self.wrapper.generateSession(
                    user_id, mpin, pyotp.TOTP(totp).now()
                )
                if response["status"] is False:
                    if "message" in response:
                        raise InvalidArgumentException(response["message"])
                    raise InvalidArgumentException("Invalid API credentials")
                token_data = self.wrapper.generateToken(self.wrapper.refresh_token)
                self.refresh_token = token_data["data"]["refreshToken"]
        except InvalidArgumentException:
            raise
        except binascii.Error:
            raise InvalidArgumentException("Invalid TOTP key provided")
        except Exception as e:
            print(e)
            raise RetryableException(str(e))

        self.user_id = user_id
        self.api_key = self.wrapper.api_key

        if load_instrument:
            self.load_instrument()

    def set_wrapper(self, serialized_wrapper):
        self.wrapper = pickle.loads(
            codecs.decode(serialized_wrapper.encode(), "base64")
        )

    def handle_exception(self, response):
        if "errorCode" in response and response["errorCode"] == "AG8001":
            raise TokenException(f"{self.user_id}: Invalid Token")

    @timeit(MetricName="Angelone:load_instrument")
    def load_instrument(self):
        try:
            self.symbol_data = InstrumentData.get_instance().load_data(
                "angelone_instruments"
            )
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from cache")
        except Exception:
            self.instrument_data = S3Utils.read_csv(
                "quantplay-market-data",
                "symbol_data/angelone_instruments.csv",
                read_from_local=False,
            )
            self.initialize_symbol_data(save_as="angelone_instruments")

        self.initialize_broker_symbol_map()

    def get_symbol(self, symbol, exchange=None):
        if exchange == "NSE":
            if symbol in ["NIFTY", "BANKNIFTY"]:
                return symbol
            if "-EQ" not in symbol:
                return f"{symbol}-EQ"
            else:
                return symbol
        if exchange == "BSE":
            return symbol

        if symbol not in self.quantplay_symbol_map:
            return symbol
        return self.quantplay_symbol_map[symbol]

    def get_order_type(self, order_type):
        if order_type == OrderType.sl:
            return AngelOne.order_sl
        elif order_type == OrderType.slm:
            return AngelOne.order_slm

        return order_type

    def get_product(self, product):
        if product == "NRML":
            return "CARRYFORWARD"
        elif product == "CNC":
            return "DELIVERY"
        elif product == "MIS":
            return "INTRADAY"
        elif product in ["BO", "MARGIN", "INTRADAY", "CARRYFORWARD", "DELIVERY"]:
            return product

        raise InvalidArgumentException(
            "Product {} not supported for trading".format(product)
        )

    @timeit(MetricName="Angelone:get_ltp")
    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def get_ltp(self, exchange=None, tradingsymbol=None):
        if tradingsymbol in MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP:
            tradingsymbol = MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP[
                tradingsymbol
            ]

        symbol_data = self.symbol_data[
            f"{exchange}:{self.get_symbol(tradingsymbol, exchange=exchange)}"
        ]
        symboltoken = symbol_data["token"]

        response = self.wrapper.ltpData(exchange, tradingsymbol, symboltoken)
        if "status" in response and response["status"] is False:
            raise InvalidArgumentException(
                "Failed to fetch ltp broker error {}".format(response)
            )

        return response["data"]["ltp"]

    @timeit(MetricName="Angelone:place_order")
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
        trigger_price=None,
    ):
        try:
            if trigger_price == 0:
                trigger_price = None

            order_type = self.get_order_type(order_type)
            product = self.get_product(product)
            tradingsymbol = self.get_symbol(tradingsymbol, exchange=exchange)
            variety = "NORMAL"
            if order_type in [AngelOne.order_sl, AngelOne.order_slm]:
                variety = "STOPLOSS"

            symbol_data = self.symbol_data[
                f"{exchange}:{self.get_symbol(tradingsymbol)}"
            ]
            symbol_token = symbol_data["token"]

            order = {
                "transactiontype": transaction_type,
                "variety": variety,
                "tradingsymbol": tradingsymbol,
                "ordertype": order_type,
                "triggerprice": trigger_price,
                "exchange": exchange,
                "symboltoken": symbol_token,
                "producttype": product,
                "price": price,
                "quantity": quantity,
                "duration": "DAY",
                "ordertag": tag,
            }

            Constants.logger.info("[PLACING_ORDER] {}".format(json.dumps(order)))
            return self.wrapper.placeOrder(order)
        except (TimeoutError, ConnectTimeout) as e:
            Constants.logger.info(f"[ANGELONE_REQUEST_TIMEOUT] {order}")
        except Exception as e:
            traceback.print_exc()
            Constants.logger.error(f"[PLACE_ORDER_FAILED] {e} {order}")
            raise QuantplayOrderPlacementException(str(e))

    def get_variety(self, variety):
        if variety == "regular":
            return "NORMAL"
        return variety

    @timeit(MetricName="Angelone:modify_order")
    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def modify_order(self, data:ModifyOrderRequest):
        try:
            orders = self.orders()
            order = orders[orders.order_id == str(data["order_id"])].to_dict("records")[
                0
            ]
            quantity = order["quantity"]
            token = order["token"]
            exchange = order["exchange"]
            product = self.get_product(order["product"])
            variety = order["variety"]
            order_type = self.get_order_type(data["order_type"])
            if "trigger_price" not in data:
                data["trigger_price"] = None
            if "quantity" in data and int(data["quantity"]) > 0:
                quantity = data["quantity"]
            order_id = data["order_id"]

            order_params = {
                "orderid": order_id,
                "variety": variety,
                "price": data["price"],
                "triggerprice": data["trigger_price"],
                "producttype": product,
                "duration": "DAY",
                "quantity": quantity,
                "symboltoken": token,
                "ordertype": order_type,
                "exchange": exchange,
                "tradingsymbol": self.get_symbol(
                    order["tradingsymbol"], exchange=exchange
                ),
            }

            Constants.logger.info(
                f"Modifying order [{order_id}] params [{order_params}]"
            )
            response = self.wrapper.modifyOrder(order_params)
            Constants.logger.info(f"[MODIFY_ORDER_RESPONSE] {response}")
            return response
        except Exception as e:
            traceback.print_exc()
            Constants.logger.error(
                f"[MODIFY_ORDER_FAILED] for {data['order_id']} failed with exception {e}"
            )
            raise

    @timeit(MetricName="Angelone:cancel_order")
    def cancel_order(self, order_id, variety="NORMAL"):
        self.wrapper.cancelOrder(order_id=order_id, variety=variety)

    @timeit(MetricName="Angelone:holdings")
    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=15000,
        stop_max_attempt_number=5,
        retry_on_exception=retry_exception,
    )
    def holdings(self):
        try:
            holdings = self.wrapper.holding()
        except:
            raise RetryableException("Access Denied retrying")
        self.handle_exception(holdings)

        if holdings["data"] is None or len(holdings["data"]) == 0:
            return pd.DataFrame(columns=self.holdings_column_list)

        holdings = pd.DataFrame(holdings["data"])
        holdings.rename(
            columns={
                "averageprice": "average_price",
                "ltp": "price",
                "symboltoken": "token",
            },
            inplace=True,
        )

        holdings["pledged_quantity"] = 0
        holdings["tradingsymbol"] = holdings["tradingsymbol"].str.replace("-EQ", "")
        holdings["buy_value"] = holdings.quantity * holdings.average_price
        holdings["current_value"] = holdings.quantity * holdings.price
        holdings["pct_change"] = (holdings.price / holdings.average_price - 1) * 100
        return holdings[self.holdings_column_list]

    @timeit(MetricName="Angelone:positions")
    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=15000,
        stop_max_attempt_number=5,
        retry_on_exception=retry_exception,
    )
    def positions(self):
        try:
            positions = self.wrapper.position()
        except:
            raise RetryableException("Access Denied retrying")
        self.handle_exception(positions)

        if positions["data"] is None:
            return pd.DataFrame(columns=self.positions_column_list)

        positions = pd.DataFrame(positions["data"])

        if "optiontype" not in positions.columns:
            positions.loc[:, "optiontype"] = None

        positions.rename(
            columns={
                "optiontype": "option_type",
                "sellqty": "sell_quantity",
                "buyqty": "buy_quantity",
                "totalsellvalue": "sell_value",
                "totalbuyvalue": "buy_value",
                "producttype": "product",
                "symboltoken": "token",
            },
            inplace=True,
        )

        positions.loc[:, "buy_quantity"] = positions.buy_quantity.astype(
            int
        ) + positions.cfbuyqty.astype(int)
        positions.loc[:, "sell_quantity"] = positions.sell_quantity.astype(
            int
        ) + positions.cfsellqty.astype(int)
        positions.loc[:, "pnl"] = positions.pnl.astype(float)
        positions.loc[:, "ltp"] = positions.ltp.astype(float)
        positions.loc[:, "quantity"] = positions.buy_quantity - positions.sell_quantity

        positions["product"] = positions["product"].replace(
            ["DELIVERY", "CARRYFORWARD", "INTRADAY"], ["CNC", "NRML", "MIS"]
        )

        existing_columns = list(positions.columns)
        columns_to_keep = list(
            set(self.positions_column_list).intersection(set(existing_columns))
        )
        return positions[columns_to_keep]

    @timeit(MetricName="Angelone:orders")
    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def orders(self, tag=None, status=None, add_ltp=True):
        try:
            order_book = self.wrapper.orderBook()
        except:
            raise RetryableException("Access Denied retrying")
        self.handle_exception(order_book)

        if order_book["data"]:
            orders = pd.DataFrame(order_book["data"])

            if len(orders) == 0:
                return pd.DataFrame(columns=self.orders_column_list)

            if add_ltp:
                positions = self.positions()
                positions = (
                    positions.sort_values("product").groupby(["tradingsymbol"]).head(1)
                )
                orders = pd.merge(
                    orders,
                    positions[["tradingsymbol", "ltp"]],
                    how="left",
                    left_on=["tradingsymbol"],
                    right_on=["tradingsymbol"],
                )
            else:
                orders.loc[:, "ltp"] = None

            orders.loc[:, "update_timestamp"] = pd.to_datetime(orders.updatetime)
            orders.rename(
                columns={
                    "orderid": "order_id",
                    "uid": self.user_id,
                    "ordertag": "tag",
                    "averageprice": "average_price",
                    "producttype": "product",
                    "transactiontype": "transaction_type",
                    "triggerprice": "trigger_price",
                    "price": "price",
                    "filledshares": "filled_quantity",
                    "unfilledshares": "pending_quantity",
                    "updatetime": "order_timestamp",
                    "info": "text",
                    "ordertype": "order_type",
                    "symboltoken": "token",
                },
                inplace=True,
            )

            existing_columns = list(orders.columns)
            columns_to_keep = list(
                set(self.orders_column_list).intersection(set(existing_columns))
            )
            orders = orders[columns_to_keep]

            orders.loc[:, "order_timestamp"] = pd.to_datetime(orders.order_timestamp)
            orders = self.filter_orders(orders, status=status, tag=tag)

            orders.status = orders.status.replace(
                ["open", "cancelled", "trigger pending", "complete", "rejected"],
                ["OPEN", "CANCELLED", "TRIGGER PENDING", "COMPLETE", "REJECTED"],
            )
            orders["product"] = orders["product"].replace(
                ["DELIVERY", "CARRYFORWARD", "INTRADAY"], ["CNC", "NRML", "MIS"]
            )
            orders["token"] = orders["token"].astype(int)
            orders["quantity"] = orders["quantity"].astype(int)
            orders["filled_quantity"] = orders["filled_quantity"].astype(int)
            orders["pending_quantity"] = orders["pending_quantity"].astype(int)

            orders["order_type"] = orders["order_type"].replace(
                [AngelOne.order_sl, AngelOne.order_slm], [OrderType.sl, OrderType.slm]
            )
            return orders
        else:
            if "message" in order_book and order_book["message"] == "SUCCESS":
                return pd.DataFrame(columns=self.orders_column_list)
            if "errorcode" in order_book and order_book["errorcode"] == "AB1010":
                raise TokenException(
                    "Can't Fetch order book because session got expired"
                )
            else:
                Constants.logger.error(order_book)
                Constants.logger.error(traceback.print_exc())
                raise ServiceException("Unknown error while fetching order book [{}]")

    @timeit(MetricName="Angelone:profile")
    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def profile(self):
        try:
            profile_data = self.wrapper.getProfile(self.refresh_token)
        except:
            raise RetryableException("Access Denied retrying")
        self.handle_exception(profile_data)

        profile_data = profile_data["data"]
        response = {
            "user_id": profile_data["clientcode"],
            "full_name": profile_data["name"],
            "email": profile_data["email"],
        }

        return response

    @timeit(MetricName="Angelone:margins")
    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def margins(self):
        api_margins = self.wrapper.rmsLimit()
        self.handle_exception(api_margins)
        if "data" in api_margins and api_margins["data"] is None:
            if "errorcode" in api_margins and api_margins["errorcode"] == "AB1004":
                raise TokenException("Angelone server not not responding")
            return {"margin_used": 0, "margin_available": 0, "total_balance": 0}
        api_margins = api_margins["data"]

        try:
            collateral = 0
            if "collateral" in api_margins:
                collateral = float(api_margins["collateral"])
            margins = {}
            margins["margin_used"] = float(api_margins["net"])
            margins["margin_available"] = float(api_margins["net"])
            margins["total_balance"] = float(api_margins["net"])

            return margins
        except (ConnectionError, ConnectTimeout) as e:
            raise BrokerException("Angelone broker error while fetching margins")
        except Exception as e:
            raise RetryableException(f"Angelone: Failed to fetch margin {e}")

    def account_summary(self):
        margins = self.margins()

        pnl = 0
        positions = self.positions()
        if len(positions) > 0:
            pnl = positions.pnl.sum()

        response = {
            "margin_used": margins["margin_used"],
            "total_balance": margins["total_balance"],
            "margin_available": margins["margin_available"],
            "pnl": pnl,
        }
        return response
