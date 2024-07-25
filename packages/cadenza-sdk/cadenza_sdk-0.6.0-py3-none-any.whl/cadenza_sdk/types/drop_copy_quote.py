# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .event import Event
from .trading.quote import Quote

__all__ = ["DropCopyQuote"]


class DropCopyQuote(Event):
    payload: Optional[Quote] = None
