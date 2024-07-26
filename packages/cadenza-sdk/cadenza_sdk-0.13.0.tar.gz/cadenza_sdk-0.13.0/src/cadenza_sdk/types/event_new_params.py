# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .market.ohlcv_param import OhlcvParam
from .trading.order_param import OrderParam
from .trading.quote_param import QuoteParam
from .market.orderbook_param import OrderbookParam
from .trading.quote_request_param import QuoteRequestParam
from .trading.execution_report_param import ExecutionReportParam
from .exchange_account_portfolio_param import ExchangeAccountPortfolioParam
from .trading.place_order_request_param import PlaceOrderRequestParam
from .trading.cancel_order_request_param import CancelOrderRequestParam

__all__ = ["EventNewParams", "Payload", "PayloadKline"]


class EventNewParams(TypedDict, total=False):
    event_id: Required[Annotated[str, PropertyInfo(alias="eventId")]]
    """A unique identifier for the event."""

    event_type: Required[
        Annotated[
            Literal[
                "cadenza.task.quoteRequestAck",
                "cadenza.task.placeOrderRequestAck",
                "cadenza.task.cancelOrderRequestAck",
                "cadenza.dropCopy.quote",
                "cadenza.dropCopy.order",
                "cadenza.dropCopy.portfolio",
                "cadenza.marketData.orderBook",
                "cadenza.marketData.kline",
            ],
            PropertyInfo(alias="eventType"),
        ]
    ]
    """Event Type"""

    timestamp: Required[int]
    """Unix timestamp in milliseconds when the event was generated."""

    payload: Payload
    """The actual data of the event, which varies based on the event type."""

    source: str
    """The source system or module that generated the event."""


class PayloadKline(TypedDict, total=False):
    candles: Iterable[OhlcvParam]

    exchange_account_id: Annotated[str, PropertyInfo(alias="exchangeAccountId")]
    """The unique identifier for the account."""

    exchange_type: Annotated[
        Literal["BINANCE", "BINANCE_MARGIN", "B2C2", "WINTERMUTE", "BLOCKFILLS", "STONEX"],
        PropertyInfo(alias="exchangeType"),
    ]
    """Exchange type"""

    interval: Literal["1s", "1m", "5m", "15m", "30m", "1h", "2h", "1d", "1w"]

    symbol: str


Payload = Union[
    QuoteRequestParam,
    PlaceOrderRequestParam,
    CancelOrderRequestParam,
    QuoteParam,
    OrderParam,
    ExecutionReportParam,
    ExchangeAccountPortfolioParam,
    OrderbookParam,
    PayloadKline,
]
