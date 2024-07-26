# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["OrderbookParam"]


class OrderbookParam(TypedDict, total=False):
    asks: Iterable[Iterable[float]]

    bids: Iterable[Iterable[float]]

    exchange_account_id: Annotated[str, PropertyInfo(alias="exchangeAccountId")]
    """UUID string"""

    exchange_type: Annotated[str, PropertyInfo(alias="exchangeType")]

    level: int
    """Order book level"""

    symbol: str
