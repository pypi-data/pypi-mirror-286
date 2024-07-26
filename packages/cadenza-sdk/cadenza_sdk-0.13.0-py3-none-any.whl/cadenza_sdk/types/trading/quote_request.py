# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["QuoteRequest"]


class QuoteRequest(BaseModel):
    base_currency: str = FieldInfo(alias="baseCurrency")
    """Base currency is the currency you want to buy or sell"""

    order_side: str = FieldInfo(alias="orderSide")
    """Order side, BUY or SELL"""

    quote_currency: str = FieldInfo(alias="quoteCurrency")
    """
    Quote currency is the currency you want to pay or receive, and the price of the
    base currency is quoted in the quote currency
    """

    exchange_account_id: Optional[str] = FieldInfo(alias="exchangeAccountId", default=None)
    """The identifier for the exchange account"""

    quantity: Optional[float] = None
    """Amount of the base currency"""

    quote_quantity: Optional[float] = FieldInfo(alias="quoteQuantity", default=None)
    """Amount of the quote currency"""
