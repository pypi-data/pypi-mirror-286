# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .event import Event
from .._models import BaseModel
from .market.ohlcv import Ohlcv
from .trading.order import Order
from .trading.quote import Quote
from .market.orderbook import Orderbook
from .trading.quote_request import QuoteRequest
from .trading.execution_report import ExecutionReport
from .exchange_account_portfolio import ExchangeAccountPortfolio
from .trading.place_order_request import PlaceOrderRequest
from .trading.cancel_order_request import CancelOrderRequest

__all__ = ["GenericEvent", "GenericEventPayload", "GenericEventPayloadKline"]


class GenericEventPayloadKline(BaseModel):
    candles: Optional[List[Ohlcv]] = None

    exchange_account_id: Optional[str] = FieldInfo(alias="exchangeAccountId", default=None)
    """The unique identifier for the account."""

    exchange_type: Optional[
        Literal["BINANCE", "BINANCE_MARGIN", "B2C2", "WINTERMUTE", "BLOCKFILLS", "STONEX"]
    ] = FieldInfo(alias="exchangeType", default=None)
    """Exchange type"""

    interval: Optional[Literal["1s", "1m", "5m", "15m", "30m", "1h", "2h", "1d", "1w"]] = None

    symbol: Optional[str] = None


GenericEventPayload = Union[
    QuoteRequest,
    PlaceOrderRequest,
    CancelOrderRequest,
    Quote,
    Order,
    ExecutionReport,
    ExchangeAccountPortfolio,
    Orderbook,
    GenericEventPayloadKline,
]


class GenericEvent(Event):
    payload: Optional[GenericEventPayload] = None
    """The actual data of the event, which varies based on the event type."""
