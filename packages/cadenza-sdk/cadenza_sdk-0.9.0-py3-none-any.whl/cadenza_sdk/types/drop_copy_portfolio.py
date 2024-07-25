# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .event import Event
from .exchange_account_portfolio import ExchangeAccountPortfolio

__all__ = ["DropCopyPortfolio"]


class DropCopyPortfolio(Event):
    payload: Optional[ExchangeAccountPortfolio] = None
