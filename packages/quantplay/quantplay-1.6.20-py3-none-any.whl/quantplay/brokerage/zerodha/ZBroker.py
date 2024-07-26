import traceback

from quantplay.brokerage.generics.broker import Broker
import pickle
import codecs
import time
from collections import defaultdict
from datetime import timedelta, datetime
from retrying import retry
import pandas as pd
from typing import List, Tuple
from quantplay.utils.data_utils import DataUtils
from quantplay.config.qplay_config import QplayConfig
from quantplay.model.exchange.instrument import QuantplayInstrument
from quantplay.model.exchange.tick import QuantplayTick
from quantplay.model.exchange.order import (
    QuantplayExchangeOrder,
    QuantplayExchangeResponseType,
    QuantplayExchangeResponse,
)
from quantplay.service import market
from alive_progress import alive_bar
from kiteconnect import KiteTicker
from quantplay.utils.constant import Constants


class DatasetPath:
    NSE_EQ = "/NSE_EQ/"
    NSE_OPT = "/NSE_OPT/"
    NSE_FUT = "/NSE_FUT/"


class ZerodhaServiceConstants:
    zerodha_token = "ZERODHA_TOKEN"
    # TODO rename it to kite_object
    zerodha_wrapper = "zerodha_wrapper"
    default_api_type = "default"


class ZBroker(Broker):
    """Zerodha Broker"""

    def __init__(self, tick_intervals, live_trade, kite=None):
        if kite:
            self.kite = kite
        else:
            kite_str = QplayConfig.get_value(ZerodhaServiceConstants.zerodha_wrapper)
            self.kite = pickle.loads(codecs.decode(kite_str.encode(), "base64"))

        self.kws = KiteTicker(self.kite.api_key, self.kite.access_token)
        try:
            self.kite.orders()
        except Exception as e:
            raise Exception(
                "Looks like token has expired. Please regenerate it through 'quantplay broker generate-token'"
            ) from e

        super(ZBroker, self).__init__(tick_intervals, live_trade)

        self.populate_instruments()

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def populate_instruments(self):
        """Calls zerodha's populate_instruments API and populates instrument mappings."""
        instruments = self.kite.instruments()
        instruments = list(
            map(
                lambda z_instrument: QuantplayInstrument.from_zerodha_instrument(
                    z_instrument
                ),
                instruments,
            )
        )

        Broker.populate_instruments(self, instruments)

    def add_strategy_symbols(self, symbols, exchange):
        super(ZBroker, self).add_strategy_symbols(symbols, exchange)
        if self.live_trade:
            Constants.logger.info("assigning callbacks")
            self.initiate_live_trade_callbacks()

    def get_all_child_orders(self):
        orders_data = self.kite.orders()
        trigger_orders = [
            QuantplayExchangeOrder.from_zerodha_order(data, is_child_order=True)
            for data in orders_data
            if data["status"] == "TRIGGER PENDING" and "tag" in data
        ]
        return trigger_orders

    def place_new_order(self, quantplay_order):
        data = quantplay_order.to_zerodha_order()
        Constants.logger.info("Placing new order through Zerodha {}".format(data))

        try:
            order_id = self.kite.place_order(
                variety=data["variety"],
                tradingsymbol=data["tradingsymbol"],
                exchange=data["exchange"],
                transaction_type=data["transaction_type"],
                quantity=int(abs(data["quantity"])),
                order_type=data["order_type"],
                disclosed_quantity=data["disclosed_quantity"],
                price=data["price"],
                trigger_price=data["trigger_price"],
                product=data["product"],
                stoploss=data["stoploss"],
                tag=data["tag"],
                squareoff=data["squareoff"],
            )
        except Exception as e:
            exception_message = (
                "Order placement failed for [{}] with error [{}]".format(
                    quantplay_order, str(e)
                )
            )
            raise Exception(exception_message) from e

        quantplay_order.order_placement_time = datetime.now()
        quantplay_order.order_id = order_id
        return order_id, quantplay_order

    def modify_existing_order(self, quantplay_order):
        data = quantplay_order.to_zerodha_order()
        order_id = quantplay_order.order_id

        try:
            response = self.kite.modify_order(
                order_id=order_id,
                variety=data["variety"],
                price=data["price"],
                trigger_price=data["trigger_price"],
                disclosed_quantity=data["disclosed_quantity"],
                order_type=data["order_type"],
            )

            Constants.logger.info(f"Successfully modified order {response}")
        except Exception as e:
            exception_message = (
                "OrderModificationFailed for {} failed with exception {}".format(
                    order_id, e
                )
            )
            raise Exception(exception_message) from e

        quantplay_order.order_placement_time = datetime.now()
        return quantplay_order

    def stream_new_symbols(self, instrument_ids):
        self.streaming_instruments = list(
            set(self.streaming_instruments + instrument_ids)
        )
        self.kws.subscribe(self.streaming_instruments)
        self.kws.set_mode(self.kws.MODE_FULL, self.streaming_instruments)

    def connect(self):
        self.kws.connect()

    def initiate_live_trade_callbacks(self):
        self.kws.on_connect = self.on_connect
        self.kws.on_ticks = self.on_ticks
        self.kws.on_order_update = self.on_order_update

    def on_connect(self, kws, response):
        """Callback on successfull connect"""
        kws.subscribe(self.streaming_instruments)
        kws.set_mode(kws.MODE_FULL, self.streaming_instruments)

    def on_ticks(self, kws, ticks):
        """Callback on live ticks"""
        quantplay_ticks = list(
            map(
                lambda t: QuantplayTick.from_zerodha_tick(
                    t,
                    self.instrument_id_to_symbol_map,
                    self.instrument_id_to_exchange_map,
                ),
                ticks,
            )
        )
        super(ZBroker, self).market_feed(quantplay_ticks)

    def on_order_update(self, kws, data):
        """Callback on order update"""
        order_id, status, status_message = (
            data["order_id"],
            data["status"],
            data["status_message"],
        )
        quantity, filled_quantity, pending_quantity = (
            data["quantity"],
            data["filled_quantity"],
            data["pending_quantity"],
        )
        average_price = data["average_price"]

        log_message = (
            f"order_id {order_id} status {status} status_message {status_message}"
        )

        Constants.logger.info(f"order_update {log_message} full_data {data}")

        last_processed_order = super(ZBroker, self).get_processed_quantplay_order_by_id(
            order_id
        )
        in_progress_order = super(ZBroker, self).get_in_progress_quantplay_order_by_id(
            order_id
        )

        responses: List[Tuple[QuantplayExchangeResponseType, int, float]] = []
        quantity = 0
        if last_processed_order:
            quantity = filled_quantity - last_processed_order.filled_quantity

        if status == "COMPLETE":
            if not last_processed_order:
                if not in_progress_order:
                    Constants.logger.info(
                        f"[DROPPING_COMPLETE_RESPONSE] order_id {order_id} not in memory"
                    )
                    return
                else:
                    responses.append(
                        (
                            QuantplayExchangeResponseType.NEW_ORDER_CONFIRM,
                            0,
                            0.0,
                        )
                    )
            responses.append(
                (
                    QuantplayExchangeResponseType.TRADE_CONFIRM,
                    quantity,
                    average_price,
                )
            )
        elif status == "UPDATE":
            if not last_processed_order:
                if not in_progress_order:
                    Constants.logger.info(
                        f"[DROPPING_UPDATE_RESPONSE] order_id {order_id} not in memory"
                    )
                    return
                elif not status_message:
                    responses.append(
                        (
                            QuantplayExchangeResponseType.NEW_ORDER_CONFIRM,
                            0,
                            0.0,
                        )
                    )
                    responses.append(
                        (
                            QuantplayExchangeResponseType.TRADE_CONFIRM,
                            quantity,
                            0.0,
                        )
                    )
                else:
                    responses.append(
                        (QuantplayExchangeResponseType.NEW_ORDER_REJECT, 0, 0.0)
                    )
            else:
                if not in_progress_order:
                    responses.append(
                        (
                            QuantplayExchangeResponseType.TRADE_CONFIRM,
                            quantity,
                            0.0,
                        )
                    )
                elif not status_message:
                    responses.append(
                        (
                            QuantplayExchangeResponseType.MOD_ORDER_CONFIRM,
                            0,
                            0.0,
                        )
                    )
                    responses.append(
                        (
                            QuantplayExchangeResponseType.TRADE_CONFIRM,
                            quantity,
                            0.0,
                        )
                    )
                else:
                    responses.append(
                        (QuantplayExchangeResponseType.MOD_ORDER_REJECT, 0, 0.0)
                    )
        elif status == "OPEN":
            if not last_processed_order:
                if not in_progress_order:
                    Constants.logger.info(
                        f"[DROPPING_OPEN_RESPONSE] order_id {order_id} not in memory"
                    )
                    return
                else:
                    responses.append(
                        (
                            QuantplayExchangeResponseType.NEW_ORDER_CONFIRM,
                            0,
                            0.0,
                        )
                    )
                    responses.append(
                        (
                            QuantplayExchangeResponseType.TRADE_CONFIRM,
                            quantity,
                            0.0,
                        )
                    )
            else:
                Constants.logger.info(f"[DROPPING_OPEN_RESPONSE] order_id {order_id}")
                return
        elif status == "REJECTED":
            if not last_processed_order:
                if not in_progress_order:
                    Constants.logger.info(
                        f"[DROPPING_REJECTED_RESPONSE] order_id {order_id} not in memory"
                    )
                    return
                else:
                    responses.append(
                        (QuantplayExchangeResponseType.NEW_ORDER_REJECT, 0, 0.0)
                    )
            else:
                if not in_progress_order:
                    Constants.logger.info(
                        f"[UNEXPECTED_REJECTED_RESPONSE] order_id {order_id}"
                    )
                    return
                else:
                    responses.append(
                        (QuantplayExchangeResponseType.MOD_ORDER_REJECT, 0, 0.0)
                    )
        elif status == "CANCELLED":
            responses.append(
                (QuantplayExchangeResponseType.CANCEL_ORDER_CONFIRM, 0, 0.0)
            )
        elif status == "TRIGGER PENDING":
            if not last_processed_order:
                if not in_progress_order:
                    Constants.logger.info(
                        f"[DROPPING_TRIGGER_PENDING_RESPONSE] order_id {order_id} not in memory"
                    )
                    return
                else:
                    responses.append(
                        (QuantplayExchangeResponseType.TRIGGER_CONFIRM, 0, 0.0)
                    )
            else:
                Constants.logger.info(
                    f"[DROPPING_TRIGGER_PENDING_RESPONSE] order_id {order_id} already in last_processed map"
                )
                return
        else:
            Constants.logger.info(
                f"[ZERODHA_UNKNOWN_STATUS] {log_message} full_data {data}"
            )
            return

        for response_type, __quantity, avg_price in responses:
            order_resp = QuantplayExchangeResponse(
                order_id, response_type, __quantity, avg_price, status_message
            )
            super(ZBroker, self).on_order_response(order_resp)

    def is_valid_live_tick(self, tick):
        today_day = datetime.now()
        if tick.exchange in ["NSE", "NFO"]:
            tick_time = tick.last_trade_time
            if (
                (tick_time.hour < 9)
                or (tick_time.hour > 15)
                or (tick_time.day != today_day.day)
                or (tick_time.hour != today_day.hour)
                or (tick_time.minute != today_day.minute)
            ):
                # print("Incorrect Trade time {}".format(tick))
                return False
            elif tick_time.hour == 9 and tick_time.minute < 15:
                self.pre_market_volume[tick.symbol] = tick.volume_traded
                return False
            elif tick_time.hour == 15 and tick_time.minute > 28:
                Constants.logger.info(
                    "Tick after 15:20 stock {} tick {}".format(tick.symbol, tick)
                )
                return False

            return True

    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=4,
    )
    def get_historical_data_from_kite(
        self, instrument, start_date, end_date, interval, continuous=False
    ):
        try:
            return self.kite.historical_data(
                instrument, start_date, end_date, interval, continuous=continuous
            )
        except Exception as e:
            print(traceback.print_exc())
            raise

    def get_historical_data(
        self, instrument, start_date, end_date, interval_max_days=None
    ):
        data_by_interval = dict()

        for interval in self.tick_intervals:
            if interval_max_days != None:
                start_date = end_date - timedelta(days=interval_max_days[interval])
                start_date = start_date.replace(minute=0, hour=0)

            if interval == "5minute":
                days_diff = 100
            elif interval == "minute":
                days_diff = 60
            elif interval == "15minute":
                days_diff = 60
            elif interval == "day":
                days_diff = 2000
            else:
                raise Exception("interval {} not whitelisted".format(interval))

            time_diff = timedelta(days=days_diff)

            data = []
            while end_date > (start_date + time_diff):
                Constants.logger.info(
                    "querying data from [%s] [%s], instrument [%s] interval [%s]"
                    % (start_date, start_date + time_diff, instrument, interval)
                )
                temp_data = self.get_historical_data_from_kite(
                    instrument,
                    start_date,
                    start_date + time_diff,
                    interval,
                    continuous=False,
                )

                start_date += time_diff

                if temp_data is not None and len(temp_data) > 0:
                    data = data + temp_data

            Constants.logger.info(
                "querying data from [%s] [%s] instrument [%s] interval [%s]"
                % (start_date, end_date, instrument, interval)
            )
            temp_data = self.get_historical_data_from_kite(
                instrument, start_date, end_date, interval, continuous=False
            )
            data = data + temp_data
            Constants.logger.info(
                "Interval {} Total size {}".format(interval, len(data))
            )

            df = pd.DataFrame(data)
            if len(df) > 0:
                symbol = self.instrument_id_to_symbol_map[instrument]
                df.loc[:, "symbol"] = symbol
                df.loc[:, "date"] = df["date"].dt.tz_localize(None)
                df.loc[:, "date"] = pd.to_datetime(df.date)

            data_by_interval[interval] = df

        return data_by_interval

    def get_equity_instruments(self, main_instruments):
        stock_list = market.symbols()
        main_instruments = [
            a for a in main_instruments if a["tradingsymbol"] in stock_list
        ]

        indices_instruments = [
            a for a in self.get_instruments() if a["segment"] == "INDICES"
        ]
        main_instruments += indices_instruments

        return main_instruments

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def filter_instruments(self, exchange, segment, name=None):
        main_instruments = self.kite.instruments()

        main_instruments = [a for a in main_instruments if a["exchange"] == exchange]
        main_instruments = [a for a in main_instruments if a["segment"] == segment]

        if name is not None:
            main_instruments = [a for a in main_instruments if name in a["name"]]

        return main_instruments
