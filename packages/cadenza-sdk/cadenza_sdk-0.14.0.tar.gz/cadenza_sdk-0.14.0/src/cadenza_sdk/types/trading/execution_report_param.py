# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo
from .order_param import OrderParam

__all__ = ["ExecutionReportParam", "Fee"]


class Fee(TypedDict, total=False):
    asset: str
    """Asset"""

    quantity: float
    """Quantity"""


class ExecutionReportParam(TypedDict, total=False):
    base_currency: Required[Annotated[str, PropertyInfo(alias="baseCurrency")]]
    """Base currency"""

    cost: Required[float]
    """Cost, the total cost of the quote"""

    created_at: Required[Annotated[int, PropertyInfo(alias="createdAt")]]
    """Create time of the quote"""

    filled: Required[float]
    """Filled quantity, the quantity of the base currency executed"""

    quote_currency: Required[Annotated[str, PropertyInfo(alias="quoteCurrency")]]
    """Quote currency"""

    route_policy: Required[Annotated[Literal["PRIORITY", "QUOTE"], PropertyInfo(alias="routePolicy")]]
    """Route policy.

    For PRIORITY, the order request will be routed to the exchange account with the
    highest priority. For QUOTE, the system will execute the execution plan based on
    the quote. Order request with route policy QUOTE will only accept two
    parameters, quoteRequestId and priceSlippageTolerance
    """

    status: Required[
        Literal[
            "SUBMITTED",
            "ACCEPTED",
            "OPEN",
            "PARTIALLY_FILLED",
            "FILLED",
            "CANCELED",
            "PENDING_CANCEL",
            "REJECTED",
            "EXPIRED",
            "REVOKED",
        ]
    ]
    """
    Status of the quote execution, should only have SUBMITTED, ACCEPTED,
    PARTIALLY_FILLED, FILLED, EXPIRED. the final status of the quote execution
    should be either FILLED or EXPIRED
    """

    updated_at: Required[Annotated[int, PropertyInfo(alias="updatedAt")]]
    """Last updated time of the quote execution"""

    cl_ord_id: Annotated[str, PropertyInfo(alias="clOrdId")]
    """Order request ID, Client Order ID"""

    executions: Iterable[OrderParam]
    """
    List of executions to fulfill the order, the order status should only have
    FILLED, REJECTED, or EXPIRED
    """

    fees: Iterable[Fee]
    """Fees"""

    order: OrderParam
