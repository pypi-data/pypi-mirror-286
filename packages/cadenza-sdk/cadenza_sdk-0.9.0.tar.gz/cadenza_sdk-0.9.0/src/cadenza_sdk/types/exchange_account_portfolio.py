# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .exchange_account_credit import ExchangeAccountCredit

__all__ = ["ExchangeAccountPortfolio", "Payload", "PayloadBalance", "PayloadPosition"]


class PayloadBalance(BaseModel):
    asset: str
    """Asset"""

    free: float
    """Free balance"""

    locked: float
    """Locked balance"""

    total: float
    """Total balance"""


class PayloadPosition(BaseModel):
    amount: float
    """Amount"""

    position_side: Literal["LONG", "SHORT"] = FieldInfo(alias="positionSide")
    """Position side"""

    status: Literal["OPEN"]
    """Status"""

    symbol: str
    """Symbol"""

    cost: Optional[float] = None
    """Cost"""

    entry_price: Optional[float] = FieldInfo(alias="entryPrice", default=None)
    """Entry price"""


class Payload(BaseModel):
    balances: List[PayloadBalance]

    credit: ExchangeAccountCredit
    """Exchange Account Credit Info"""

    exchange_account_id: str = FieldInfo(alias="exchangeAccountId")
    """The unique identifier for the account."""

    exchange_type: Literal["BINANCE", "BINANCE_MARGIN", "B2C2", "WINTERMUTE", "BLOCKFILLS", "STONEX"] = FieldInfo(
        alias="exchangeType"
    )
    """Exchange type"""

    positions: List[PayloadPosition]

    updated_at: int = FieldInfo(alias="updatedAt")
    """The timestamp when the portfolio information was updated."""


class ExchangeAccountPortfolio(BaseModel):
    payload: Optional[Payload] = None
