# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .event import Event
from .trading.order import Order

__all__ = ["DropCopyOrder"]


class DropCopyOrder(Event):
    event_type: Optional[Literal["cadenza.dropCopy.order"]] = FieldInfo(alias="eventType", default=None)

    payload: Optional[Order] = None
