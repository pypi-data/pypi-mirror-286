# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo
from ..trading.place_order_request_param import PlaceOrderRequestParam

__all__ = ["TaskTaskPlaceOrderRequestAckParams"]


class TaskTaskPlaceOrderRequestAckParams(TypedDict, total=False):
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

    payload: PlaceOrderRequestParam

    source: str
    """The source system or module that generated the event."""
