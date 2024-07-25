# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["Quote"]


class Quote(BaseModel):
    base_currency: str = FieldInfo(alias="baseCurrency")
    """Base currency"""

    quote_currency: str = FieldInfo(alias="quoteCurrency")
    """Quote currency"""

    quote_request_id: str = FieldInfo(alias="quoteRequestId")
    """Quote request ID"""

    timestamp: int
    """Create time of the quote"""

    valid_until: int = FieldInfo(alias="validUntil")
    """Expiration time of the quote"""

    ask_price: Optional[float] = FieldInfo(alias="askPrice", default=None)
    """Ask price"""

    ask_quantity: Optional[float] = FieldInfo(alias="askQuantity", default=None)
    """Ask quantity"""

    bid_price: Optional[float] = FieldInfo(alias="bidPrice", default=None)
    """Bid price"""

    bid_quantity: Optional[float] = FieldInfo(alias="bidQuantity", default=None)
    """Bid quantity"""

    exchange_account_id: Optional[str] = FieldInfo(alias="exchangeAccountId", default=None)
    """Exchange Account ID"""

    exchange_type: Optional[
        Literal["BINANCE", "BINANCE_MARGIN", "B2C2", "WINTERMUTE", "BLOCKFILLS", "STONEX"]
    ] = FieldInfo(alias="exchangeType", default=None)
    """Exchange type"""
