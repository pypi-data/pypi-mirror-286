# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["OrderParam"]


class OrderParam(TypedDict, total=False):
    cost: Required[float]
    """The total cost of this order."""

    created_at: Required[Annotated[int, PropertyInfo(alias="createdAt")]]
    """Created timestamp"""

    exchange_account_id: Required[Annotated[str, PropertyInfo(alias="exchangeAccountId")]]
    """Exchange account ID"""

    exchange_type: Required[
        Annotated[
            Literal["BINANCE", "BINANCE_MARGIN", "B2C2", "WINTERMUTE", "BLOCKFILLS", "STONEX"],
            PropertyInfo(alias="exchangeType"),
        ]
    ]
    """Exchange type"""

    filled: Required[float]
    """The quantity of this order that has been filled."""

    order_side: Required[Annotated[Literal["BUY", "SELL"], PropertyInfo(alias="orderSide")]]
    """Order side"""

    order_type: Required[
        Annotated[
            Literal["MARKET", "LIMIT", "STOP_LOSS", "STOP_LOSS_LIMIT", "TAKE_PROFIT", "TAKE_PROFIT_LIMIT", "QUOTED"],
            PropertyInfo(alias="orderType"),
        ]
    ]
    """Order type"""

    quantity: Required[float]
    """Quantity"""

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
    """Order status"""

    symbol: Required[str]
    """Symbol"""

    time_in_force: Required[
        Annotated[
            Literal["DAY", "GTC", "GTX", "GTD", "OPG", "CLS", "IOC", "FOK", "GFA", "GFS", "GTM", "MOO", "MOC", "EXT"],
            PropertyInfo(alias="timeInForce"),
        ]
    ]
    """Time in force"""

    updated_at: Required[Annotated[int, PropertyInfo(alias="updatedAt")]]
    """Last updated timestamp"""

    fee: float
    """Fee"""

    fee_currency: Annotated[str, PropertyInfo(alias="feeCurrency")]
    """Fee currency"""

    order_id: Annotated[str, PropertyInfo(alias="orderId")]

    position_id: Annotated[str, PropertyInfo(alias="positionId")]
    """Position ID"""

    price: float
    """Price"""

    quote_quantity: Annotated[float, PropertyInfo(alias="quoteQuantity")]
    """Quote Quantity"""

    tenant_id: Annotated[str, PropertyInfo(alias="tenantId")]
    """Tenant ID"""

    user_id: Annotated[str, PropertyInfo(alias="userId")]
    """User ID"""
