# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .exchange_account_credit_param import ExchangeAccountCreditParam

__all__ = ["ExchangeAccountPortfolioParam", "Balance", "Position"]


class Balance(TypedDict, total=False):
    asset: Required[str]
    """Asset"""

    borrowed: float
    """Borrowed balance from exchange"""

    free: float
    """Free balance"""

    locked: float
    """Locked balance"""

    net: float
    """Net Balance, net = total - borrowed"""

    total: float
    """Total available balance"""


class Position(TypedDict, total=False):
    amount: Required[float]
    """Amount"""

    position_side: Required[Annotated[Literal["LONG", "SHORT"], PropertyInfo(alias="positionSide")]]
    """Position side"""

    status: Required[Literal["OPEN"]]
    """Status"""

    symbol: Required[str]
    """Symbol"""

    cost: float
    """Cost"""

    entry_price: Annotated[float, PropertyInfo(alias="entryPrice")]
    """Entry price"""


class ExchangeAccountPortfolioParam(TypedDict, total=False):
    credit: Required[ExchangeAccountCreditParam]
    """Exchange Account Credit Info"""

    exchange_account_id: Required[Annotated[str, PropertyInfo(alias="exchangeAccountId")]]
    """The unique identifier for the account."""

    exchange_type: Required[
        Annotated[
            Literal["BINANCE", "BINANCE_MARGIN", "B2C2", "WINTERMUTE", "BLOCKFILLS", "STONEX"],
            PropertyInfo(alias="exchangeType"),
        ]
    ]
    """Exchange type"""

    updated_at: Required[Annotated[int, PropertyInfo(alias="updatedAt")]]
    """The timestamp when the portfolio information was updated."""

    balances: Iterable[Balance]

    positions: Iterable[Position]
