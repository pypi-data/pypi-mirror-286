# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["QuoteWithOrderCandidatesParam", "OrderCandidate"]


class OrderCandidate(TypedDict, total=False):
    exchange_account_id: Annotated[str, PropertyInfo(alias="exchangeAccountId")]
    """Exchange account ID"""

    order_side: Annotated[Literal["BUY", "SELL"], PropertyInfo(alias="orderSide")]
    """Order side"""

    order_type: Annotated[
        Literal["MARKET", "LIMIT", "STOP_LOSS", "STOP_LOSS_LIMIT", "TAKE_PROFIT", "TAKE_PROFIT_LIMIT", "QUOTED"],
        PropertyInfo(alias="orderType"),
    ]
    """Order type"""

    quantity: float
    """Quantity"""

    quote_quantity: Annotated[float, PropertyInfo(alias="quoteQuantity")]
    """Quote Quantity"""

    quote_request_id: Annotated[str, PropertyInfo(alias="quoteRequestId")]
    """Quote request ID"""

    route_policy: Annotated[Literal["PRIORITY", "QUOTE"], PropertyInfo(alias="routePolicy")]
    """Route policy.

    For PRIORITY, the order request will be routed to the exchange account with the
    highest priority. For QUOTE, the system will execute the execution plan based on
    the quote. Order request with route policy QUOTE will only accept two
    parameters, quoteRequestId and priceSlippageTolerance
    """

    symbol: str
    """Symbol"""


class QuoteWithOrderCandidatesParam(TypedDict, total=False):
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

    order_candidates: Annotated[Iterable[OrderCandidate], PropertyInfo(alias="orderCandidates")]
