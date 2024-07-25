# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["QuoteParam"]


class QuoteParam(TypedDict, total=False):
    base_currency: Required[Annotated[str, PropertyInfo(alias="baseCurrency")]]
    """Base currency"""

    quote_currency: Required[Annotated[str, PropertyInfo(alias="quoteCurrency")]]
    """Quote currency"""

    quote_request_id: Required[Annotated[str, PropertyInfo(alias="quoteRequestId")]]
    """Quote request ID"""

    timestamp: Required[int]
    """Create time of the quote"""

    valid_until: Required[Annotated[int, PropertyInfo(alias="validUntil")]]
    """Expiration time of the quote"""

    ask_price: Annotated[float, PropertyInfo(alias="askPrice")]
    """Ask price"""

    ask_quantity: Annotated[float, PropertyInfo(alias="askQuantity")]
    """Ask quantity"""

    bid_price: Annotated[float, PropertyInfo(alias="bidPrice")]
    """Bid price"""

    bid_quantity: Annotated[float, PropertyInfo(alias="bidQuantity")]
    """Bid quantity"""

    exchange_account_id: Annotated[str, PropertyInfo(alias="exchangeAccountId")]
    """Exchange Account ID"""

    exchange_type: Annotated[
        Literal["BINANCE", "BINANCE_MARGIN", "B2C2", "WINTERMUTE", "BLOCKFILLS", "STONEX"],
        PropertyInfo(alias="exchangeType"),
    ]
    """Exchange type"""
