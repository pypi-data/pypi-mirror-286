# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo
from ..trading.quote_param import QuoteParam

__all__ = ["EventDropCopyQuoteParams"]


class EventDropCopyQuoteParams(TypedDict, total=False):
    event_id: Required[Annotated[str, PropertyInfo(alias="eventId")]]
    """A unique identifier for the event."""

    event_type: Required[Annotated[str, PropertyInfo(alias="eventType")]]
    """The type of the event (e.g., order, executionReport, portfolio, orderBook)."""

    timestamp: Required[int]
    """Unix timestamp in milliseconds when the event was generated."""

    payload: QuoteParam

    source: str
    """The source system or module that generated the event."""
