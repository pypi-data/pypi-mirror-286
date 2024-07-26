import os
import traceback

import pandas as pd
from pya3 import Aliceblue as Alice
from pya3 import OrderType as AliceOrderType
from pya3 import ProductType
from pya3 import TransactionType
from retrying import retry
import numpy as np
import pickle, codecs
from retrying import retry

from quantplay.wrapper.aws.s3 import S3Utils
from quantplay.broker.generics.broker import Broker
from quantplay.exception.exceptions import InvalidArgumentException, TokenException
from quantplay.exception.exceptions import (
    QuantplayOrderPlacementException,
    RetryableException,
    retry_exception,
)
from quantplay.utils.constant import Constants, OrderType, OrderStatus, timeit
from quantplay.utils.pickle_utils import InstrumentData

logger = Constants.logger


class Aliceblue(Broker):
    @timeit(MetricName="Aliceblue:__init__")
    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=2,
        retry_on_exception=retry_exception,
    )
    def __init__(self, user_id=None, api_key=None, order_updates=None, client=None):
        super(Aliceblue, self).__init__()
        self.order_updates = order_updates

        try:
            if client:
                self.set_client(client)
            else:
                if user_id is None or api_key is None:
                    raise InvalidArgumentException(
                        "Mandatory fields [user_id/api_key] are missing"
                    )
                self.alice = Alice(
                    user_id=user_id,
                    api_key=api_key,
                )
                response = self.alice.get_session_id()
                if "sessionID" not in response or response["sessionID"] is None:
                    if "emsg" in response:
                        if response["emsg"].lower() == "invalid input":
                            response["emsg"] = "Invalid broker credentials"
                        raise InvalidArgumentException(response["emsg"])
                    raise InvalidArgumentException(f"Invalid API Key {api_key}")
        except (InvalidArgumentException, TokenException) as e:
            raise
        except Exception as e:
            raise RetryableException(str(e))
        self.user_id = self.alice.user_id
        self.load_instrument()

    def set_client(self, serialized_client):
        try:
            self.alice = pickle.loads(
                codecs.decode(serialized_client.encode(), "base64")
            )
        except Exception as e:
            raise TokenException(f"Session expired")

    def set_attributes(self, response):
        self.email = response["email"]
        self.user_id = response["actid"]
        self.full_name = response["uname"]
        self.user_token = response["susertoken"]

    def get_quantplay_symbol(self, symbol):
        if "-EQ" in symbol:
            return symbol.replace("-EQ", "")
        return symbol

    def get_symbol(self, symbol, exchange=None):
        if exchange == "NSE":
            if "-EQ" not in symbol:
                return f"{symbol}-EQ"
        elif symbol not in self.quantplay_symbol_map:
            return symbol
        return self.quantplay_symbol_map[symbol]

    @timeit(MetricName="Aliceblue:load_instrument")
    def load_instrument(self):
        try:
            self.symbol_data = InstrumentData.get_instance().load_data(
                "aliceblue_instruments"
            )
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from cache")
        except Exception:
            self.instrument_data = S3Utils.read_csv(
                "quantplay-market-data",
                "symbol_data/aliceblue_instruments.csv",
                read_from_local=False,
            )
            self.initialize_symbol_data(save_as="aliceblue_instruments")

        self.initialize_broker_symbol_map()

    def get_transaction_type(self, transaction_type):
        if (
            transaction_type == "BUY"
            or transaction_type == TransactionType.Buy.value
            or transaction_type == "B"
        ):
            return TransactionType.Buy
        elif (
            transaction_type == "SELL"
            or transaction_type == TransactionType.Sell.value
            or transaction_type == "S"
        ):
            return TransactionType.Sell

        raise InvalidArgumentException(
            "transaction type {} not supported for trading".format(transaction_type)
        )

    def get_order_type(self, order_type):
        if order_type == OrderType.market or order_type == AliceOrderType.Market.value:
            return AliceOrderType.Market
        elif (
            order_type == OrderType.sl
            or order_type == AliceOrderType.StopLossLimit.value
        ):
            return AliceOrderType.StopLossLimit
        elif (
            order_type == OrderType.slm
            or order_type == AliceOrderType.StopLossMarket.value
        ):
            return AliceOrderType.StopLossMarket
        elif order_type == OrderType.limit or order_type == AliceOrderType.Limit.value:
            return AliceOrderType.Limit

        return order_type

    def get_product(self, product):
        if product == "NRML":
            return ProductType.Normal
        elif product == "CNC":
            return ProductType.Delivery
        elif product == "MIS":
            return ProductType.Intraday
        elif product in [
            ProductType.BracketOrder,
            ProductType.CoverOrder,
            ProductType.Delivery,
            ProductType.Normal,
            ProductType.Intraday,
        ]:
            return product

        raise InvalidArgumentException(
            "Product {} not supported for trading".format(product)
        )

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
            if trigger_price != None:
                trigger_price = float(trigger_price)

            order_type = self.get_order_type(order_type)
            product = self.get_product(product)
            tradingsymbol = self.get_symbol(tradingsymbol)

            instrument = self.alice.get_instrument_by_symbol(exchange, tradingsymbol)

            response = self.alice.place_order(
                transaction_type=self.get_transaction_type(transaction_type),
                product_type=product,
                instrument=instrument,
                order_type=order_type,
                quantity=quantity,
                price=float(price),
                trigger_price=trigger_price,
                order_tag=tag,
            )
            Constants.logger.info(f"[PLACE_ORDER_RESPONSE] {response}")
            return response["NOrdNo"]
        except Exception as e:
            print(traceback.print_exc())
            exception_message = f"Order placement failed [{str(e)}]"
            raise QuantplayOrderPlacementException(exception_message)

    def get_ltp(self, exchange, tradingsymbol):
        inst = self.alice.get_instrument_by_symbol(exchange, tradingsymbol)
        info = self.alice.get_scrip_info(inst)
        return float(info["LTP"])

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def modify_order(self, data):
        try:
            order_id = data["order_id"]
            order_history = self.alice.get_order_history(order_id)
            exchange = order_history["Exchange"]
            token = int(order_history["token"])
            product_type = self.get_product(order_history["Pcode"])
            quantity = order_history["Qty"]

            order_type = order_history["Prctype"]
            if "order_type" in data:
                order_type = data["order_type"]
            order_type = self.get_order_type(order_type)

            transaction_type = order_history["Trantype"]
            if "transaction_type" in data:
                transaction_type = data["transaction_type"]
            transaction_type = self.get_transaction_type(transaction_type)

            trigger_price = None
            if "trigger_price" in data and data["trigger_price"] is not None:
                trigger_price = float(data["trigger_price"])

            response = self.alice.modify_order(
                instrument=self.alice.get_instrument_by_token(exchange, token),
                transaction_type=transaction_type,
                order_id=order_id,
                product_type=product_type,
                order_type=order_type,
                price=float(data["price"]),
                trigger_price=trigger_price,
                quantity=quantity,
            )
            logger.info("[MODIFY_ORDER_RESPONSE] [{order_id}]  response [{response}]")
            return response
        except Exception as e:
            print(traceback.print_exc())
            Constants.logger.error(
                f"[MODIFY_ORDER_FAILED] {data} with exception {str(e)}"
            )

    def modify_price(self, order_id, price, trigger_price=None, order_type=None):
        data = {}

        data["order_id"] = order_id
        data["price"] = price
        data["order_type"] = order_type
        if trigger_price is not None and trigger_price > 0:
            data["trigger_price"] = trigger_price
        else:
            data["trigger_price"] = None

        self.modify_order(data)

    def cancel_order(self, order_id):
        return self.alice.cancel_order(order_id)

    def profile(self):
        profile = self.alice.get_profile()
        response = {
            "user_id": self.alice.user_id,
            "full_name": profile["accountName"],
            "email": profile["emailAddr"],
        }

        return response

    @timeit(MetricName="Aliceblue:holdings")
    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def holdings(self):
        holdings = self.alice.get_holding_positions()
        if "HoldingVal" not in holdings or len(holdings["HoldingVal"]) == 0:
            return pd.DataFrame(columns=self.holdings_column_list)
        holdings = holdings["HoldingVal"]
        holdings = pd.DataFrame(holdings)
        holdings = holdings[holdings.ExchSeg1 == "NSE"]

        holdings.rename(
            columns={
                "Nsetsym": "tradingsymbol",
                "Token1": "token",
                "Price": "average_price",
                "HUqty": "quantity",
            },
            inplace=True,
        )
        holdings["quantity"] = holdings.quantity.astype(int)
        holdings["average_price"] = holdings.average_price.astype(float)
        holdings["pledged_quantity"] = 0
        holdings["exchange"] = "NSE"
        holdings["price"] = holdings.apply(
            lambda x: self.get_ltp(x["exchange"], x["tradingsymbol"]), axis=1
        )
        holdings["buy_value"] = holdings.quantity * holdings.average_price
        holdings["current_value"] = holdings.quantity * holdings.price
        holdings["pct_change"] = (holdings.price / holdings.average_price - 1) * 100
        holdings["tradingsymbol"] = holdings["tradingsymbol"].str.replace("-EQ", "")

        return holdings[self.holdings_column_list]

    @timeit(MetricName="Aliceblue:positions")
    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def positions(self):
        positions = self.alice.get_netwise_positions()

        if not isinstance(positions, list):
            return pd.DataFrame(columns=self.positions_column_list)

        positions = pd.DataFrame(positions)
        positions.loc[:, "pnl"] = positions.realisedprofitloss.astype(
            float
        ) + positions.unrealisedprofitloss.astype(float)

        positions.rename(
            columns={
                "LTP": "ltp",
                "Tsym": "tradingsymbol",
                "Opttype": "option_type",
                "Pcode": "product",
                "netsellqty": "sell_quantity",
                "netbuyqty": "buy_quantity",
                "Exchange": "exchange",
                "Token": "token",
                "netbuyamt": "buy_value",
                "netSellamt": "sell_value",
            },
            inplace=True,
        )

        positions["ltp"] = positions.ltp.astype(float)
        positions["buy_quantity"] = positions.buy_quantity.astype(int)
        positions["sell_quantity"] = positions.sell_quantity.astype(int)
        positions["quantity"] = positions.buy_quantity - positions.sell_quantity
        positions["average_price"] = np.where(
            positions.quantity > 0, positions.NetBuyavgprc, positions.NetSellavgprc
        )
        positions["average_price"] = np.where(
            positions.quantity == 0, 0, positions.average_price
        )

        positions["average_price"] = positions["average_price"].astype(float)
        return positions[self.positions_column_list]

    def orders(self, tag=None, status=None, add_ltp=True):
        orders = self.alice.order_data()
        if not isinstance(orders, list) and (
            ("no data" in orders["emsg"].lower())
            or ("401" in orders["emsg"].lower() or ("404" in orders["emsg"]))
        ):
            return pd.DataFrame(columns=self.orders_column_list)
        positions = self.positions()
        positions = positions.sort_values("product").groupby(["tradingsymbol"]).head(1)
        if len(orders) == 0:
            return pd.DataFrame(columns=self.orders_column_list)

        orders = pd.DataFrame(orders)
        orders.loc[:, "tradingsymbol"] = orders.Trsym

        orders = pd.merge(
            orders,
            positions[["tradingsymbol", "ltp"]],
            how="left",
            left_on=["tradingsymbol"],
            right_on=["tradingsymbol"],
        )

        orders.rename(
            columns={
                "Nstordno": "order_id",
                "accountId": "user_id",
                "Exchange": "exchange",
                "Avgprc": "average_price",
                "Pcode": "product",
                "Trantype": "transaction_type",
                "Qty": "quantity",
                "Trgprc": "trigger_price",
                "Prc": "price",
                "Fillshares": "filled_quantity",
                "rorgqty": "pending_quantity",
                "OrderedTime": "update_timestamp",
                "orderentrytime": "order_timestamp",
                "Prctype": "order_type",
                "Status": "status",
            },
            inplace=True,
        )

        if "filled_quantity" not in orders.columns:
            orders.loc[:, "filled_quantity"] = 0
        if "average_price" not in orders.columns:
            orders.loc[:, "average_price"] = 0
        orders["filled_quantity"] = orders.filled_quantity.astype(float)
        orders["average_price"] = orders.average_price.astype(float)
        orders.loc[:, "pnl"] = (
            orders.ltp * orders.filled_quantity
            - orders.average_price * orders.filled_quantity
        )
        orders.loc[:, "pnl"] = np.where(
            orders.transaction_type == "S", -orders.pnl, orders.pnl
        )
        orders["order_timestamp"] = pd.to_datetime(orders.order_timestamp)
        orders["update_timestamp"] = pd.to_datetime(
            orders.update_timestamp, format="%d/%m/%Y %H:%M:%S"
        )

        orders.transaction_type = orders.transaction_type.replace(
            ["S", "B"], ["SELL", "BUY"]
        )

        orders.status = orders.status.replace(
            ["open", "trigger pending", "rejected", "cancelled", "complete"],
            [
                OrderStatus.open,
                OrderStatus.trigger_pending,
                OrderStatus.rejected,
                OrderStatus.cancelled,
                OrderStatus.complete,
            ],
        )

        orders.order_type = orders.order_type.replace(
            ["MKT", "L", "SL"], [OrderType.market, OrderType.limit, OrderType.sl]
        )

        orders = self.filter_orders(orders, status=status, tag=tag)
        for col in [
            "tag",
            "pending_quantity",
            "variety",
            "status_message",
            "status_message_raw",
        ]:
            orders[col] = None
        return orders[self.orders_column_list]

    def margins(self):
        margins = self.alice.get_balance()
        if "emsg" in margins and "expired" in margins["emsg"].lower():
            raise TokenException("Session expired")
        if "stat" in margins and "not_ok" in margins["stat"].lower():
            raise TokenException(f"Aliceblue broker error: {margins['emsg']}")
        margins = [a for a in margins if a["segment"] == "ALL"][0]

        response = {
            "margin_used": float(margins["debits"]),
            "total_balance": float(margins["credits"]),
            "margin_available": float(margins["net"]),
        }
        return response

    def account_summary(self):
        margins = self.margins()

        margins["pnl"] = float(self.positions().pnl.sum())
        return margins
