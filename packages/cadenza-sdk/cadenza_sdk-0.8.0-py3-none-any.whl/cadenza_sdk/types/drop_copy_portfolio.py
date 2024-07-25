# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .event import Event
from .exchange_account_portfolio import ExchangeAccountPortfolio

__all__ = ["DropCopyPortfolio"]


class DropCopyPortfolio(Event):
    event_type: Optional[Literal["cadenza.dropCopy.portfolio"]] = FieldInfo(alias="eventType", default=None)

    payload: Optional[ExchangeAccountPortfolio] = None
