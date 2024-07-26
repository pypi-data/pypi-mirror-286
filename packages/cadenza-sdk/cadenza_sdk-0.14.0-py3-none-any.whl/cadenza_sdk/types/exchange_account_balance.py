# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ExchangeAccountBalance", "Balance"]


class Balance(BaseModel):
    asset: str
    """Asset"""

    borrowed: Optional[float] = None
    """Borrowed balance from exchange"""

    free: Optional[float] = None
    """Free balance"""

    locked: Optional[float] = None
    """Locked balance"""

    net: Optional[float] = None
    """Net Balance, net = total - borrowed"""

    total: Optional[float] = None
    """Total available balance"""


class ExchangeAccountBalance(BaseModel):
    balances: List[Balance]
    """List of balances"""

    exchange_account_id: str = FieldInfo(alias="exchangeAccountId")
    """Exchange account ID"""
