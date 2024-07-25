# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, Annotated, TypedDict

from .._types import Base64FileInput
from .._utils import PropertyInfo
from .._models import set_pydantic_config

__all__ = ["WebhookPubsubParams", "Message"]


class WebhookPubsubParams(TypedDict, total=False):
    message: Required[Message]

    subscription: Required[str]
    """The subscription name."""


class Message(TypedDict, total=False):
    id: Required[str]
    """The unique identifier for the message."""

    data: Annotated[Union[str, Base64FileInput], PropertyInfo(format="base64")]
    """The base64-encoded data."""


set_pydantic_config(Message, {"arbitrary_types_allowed": True})
