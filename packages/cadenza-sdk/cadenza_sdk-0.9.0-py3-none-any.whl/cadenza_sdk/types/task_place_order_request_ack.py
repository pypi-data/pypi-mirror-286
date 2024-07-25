# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .event import Event
from .trading.place_order_request import PlaceOrderRequest

__all__ = ["TaskPlaceOrderRequestAck"]


class TaskPlaceOrderRequestAck(Event):
    payload: Optional[PlaceOrderRequest] = None
