# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo
from ..market.ohlcv_param import OhlcvParam

__all__ = ["MarketDataMarketDataKlineParams", "Payload"]


class MarketDataMarketDataKlineParams(TypedDict, total=False):
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

    source: str
    """The source system or module that generated the event."""


class Payload(TypedDict, total=False):
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
