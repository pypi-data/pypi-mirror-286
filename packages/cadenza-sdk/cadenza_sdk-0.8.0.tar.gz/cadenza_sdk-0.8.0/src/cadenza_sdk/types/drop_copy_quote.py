# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .event import Event
from .trading.quote import Quote

__all__ = ["DropCopyQuote"]


class DropCopyQuote(Event):
    event_type: Optional[Literal["cadenza.dropCopy.quote"]] = FieldInfo(alias="eventType", default=None)

    payload: Optional[Quote] = None
