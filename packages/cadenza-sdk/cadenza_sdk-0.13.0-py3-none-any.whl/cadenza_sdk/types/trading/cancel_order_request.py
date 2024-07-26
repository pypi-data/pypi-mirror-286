# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["CancelOrderRequest"]


class CancelOrderRequest(BaseModel):
    order_id: str = FieldInfo(alias="orderId")
    """Order ID"""
