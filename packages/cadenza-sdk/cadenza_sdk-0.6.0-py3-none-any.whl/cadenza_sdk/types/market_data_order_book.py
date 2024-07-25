# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .event import Event
from .market.orderbook import Orderbook

__all__ = ["MarketDataOrderBook"]


class MarketDataOrderBook(Event):
    payload: Optional[Orderbook] = None
