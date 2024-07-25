# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .event import Event
from .trading.order import Order

__all__ = ["DropCopyOrder"]


class DropCopyOrder(Event):
    payload: Optional[Order] = None
