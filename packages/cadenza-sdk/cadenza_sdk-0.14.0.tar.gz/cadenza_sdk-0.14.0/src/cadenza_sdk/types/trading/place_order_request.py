# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["PlaceOrderRequest"]


class PlaceOrderRequest(BaseModel):
    route_policy: Literal["PRIORITY", "QUOTE"] = FieldInfo(alias="routePolicy")
    """Route policy.

    For PRIORITY, the order request will be routed to the exchange account with the
    highest priority. For QUOTE, the system will execute the execution plan based on
    the quote. Order request with route policy QUOTE will only accept two
    parameters, quoteRequestId and priceSlippageTolerance
    """

    exchange_account_id: Optional[str] = FieldInfo(alias="exchangeAccountId", default=None)
    """Exchange account ID"""

    leverage: Optional[int] = None
    """Levarage"""

    order_side: Optional[Literal["BUY", "SELL"]] = FieldInfo(alias="orderSide", default=None)
    """Order side"""

    order_type: Optional[
        Literal["MARKET", "LIMIT", "STOP_LOSS", "STOP_LOSS_LIMIT", "TAKE_PROFIT", "TAKE_PROFIT_LIMIT", "QUOTED"]
    ] = FieldInfo(alias="orderType", default=None)
    """Order type"""

    position_id: Optional[str] = FieldInfo(alias="positionId", default=None)
    """Position ID for closing position in margin trading"""

    price: Optional[float] = None
    """Price"""

    price_slippage_tolerance: Optional[float] = FieldInfo(alias="priceSlippageTolerance", default=None)
    """Price slippage tolerance, range: [0, 0.1] with 2 decimal places"""

    priority: Optional[List[str]] = None
    """Priority list of exchange account ID in descending order"""

    quantity: Optional[float] = None
    """Quantity.

    One of quantity or quoteQuantity must be provided. If both is provided, only
    quantity will be used.
    """

    quote_id: Optional[str] = FieldInfo(alias="quoteId", default=None)
    """Quote ID used by exchange for RFQ, e.g.

    WINTERMUTE need this field to execute QUOTED order
    """

    quote_quantity: Optional[float] = FieldInfo(alias="quoteQuantity", default=None)
    """Quote Quantity"""

    quote_request_id: Optional[str] = FieldInfo(alias="quoteRequestId", default=None)
    """Quote request ID"""

    symbol: Optional[str] = None
    """Symbol"""

    tenant_id: Optional[str] = FieldInfo(alias="tenantId", default=None)
    """Tenant ID"""

    time_in_force: Optional[
        Literal["DAY", "GTC", "GTX", "GTD", "OPG", "CLS", "IOC", "FOK", "GFA", "GFS", "GTM", "MOO", "MOC", "EXT"]
    ] = FieldInfo(alias="timeInForce", default=None)
    """Time in force"""
