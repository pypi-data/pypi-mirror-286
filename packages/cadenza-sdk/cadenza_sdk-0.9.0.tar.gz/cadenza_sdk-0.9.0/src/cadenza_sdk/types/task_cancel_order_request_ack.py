# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .event import Event
from .trading.cancel_order_request import CancelOrderRequest

__all__ = ["TaskCancelOrderRequestAck"]


class TaskCancelOrderRequestAck(Event):
    payload: Optional[CancelOrderRequest] = None
