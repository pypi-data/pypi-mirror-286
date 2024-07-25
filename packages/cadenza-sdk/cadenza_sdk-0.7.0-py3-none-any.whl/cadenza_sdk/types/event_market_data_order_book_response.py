# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .event import Event
from .market.orderbook import Orderbook

__all__ = ["EventMarketDataOrderBookResponse"]


class EventMarketDataOrderBookResponse(Event):
    event_type: Optional[Literal["cadenza.marketData.orderBook"]] = FieldInfo(alias="eventType", default=None)

    payload: Optional[Orderbook] = None
