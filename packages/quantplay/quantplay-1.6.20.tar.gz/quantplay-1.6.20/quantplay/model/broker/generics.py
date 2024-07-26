from typing import Literal, TypedDict
from typing_extensions import NotRequired

ExchangeType = Literal["NFO", "BFO", "NSE", "BSE", "MCX", "NCD", "BCD", "MFO"]
ProductType = Literal["NRML", "MIS", "CNC"]
OrderType = Literal["MARKET", "LIMIT", "SL"]
TransactionType = Literal["SELL", "BUY"]
InstrumentType = Literal["CE", "PE", "EQ", "FUT"]
StatusType = Literal["COMPLETE", "REJECTED", "CANCELLED", "TRIGGER PENDING", "OPEN"]


class ModifyOrderRequest(TypedDict):
    order_id: str
    quantity: int
    exchange: ExchangeType
    trigger_price: float
    order_type: OrderType
    price: float


class UserBrokerProfileResponse(TypedDict):
    user_id: str
    full_name: str
    segments: NotRequired[ExchangeType]
    exchanges: NotRequired[ExchangeType]
    email: NotRequired[str]
