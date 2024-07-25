# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .event import Event
from .trading.quote_request import QuoteRequest

__all__ = ["TaskQuoteRequestAck"]


class TaskQuoteRequestAck(Event):
    payload: Optional[QuoteRequest] = None
