# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["OhlcvParam"]


class OhlcvParam(TypedDict, total=False):
    c: float
    """Close price"""

    h: float
    """High price"""

    l: float
    """Low price"""

    o: float
    """Open price"""

    t: int
    """Start time (in unix milliseconds)"""

    v: float
    """Volume"""
