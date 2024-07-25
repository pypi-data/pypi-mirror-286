# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .event import Event
from .._models import BaseModel
from .market.ohlcv import Ohlcv

__all__ = ["EventMarketDataKlineResponse", "EventMarketDataKlineResponsePayload"]


class EventMarketDataKlineResponsePayload(BaseModel):
    candles: Optional[List[Ohlcv]] = None

    exchange_account_id: Optional[str] = FieldInfo(alias="exchangeAccountId", default=None)
    """The unique identifier for the account."""

    exchange_type: Optional[
        Literal["BINANCE", "BINANCE_MARGIN", "B2C2", "WINTERMUTE", "BLOCKFILLS", "STONEX"]
    ] = FieldInfo(alias="exchangeType", default=None)
    """Exchange type"""

    interval: Optional[Literal["1s", "1m", "5m", "15m", "30m", "1h", "2h", "1d", "1w"]] = None

    symbol: Optional[str] = None


class EventMarketDataKlineResponse(Event):
    event_type: Optional[Literal["cadenza.marketData.kline"]] = FieldInfo(alias="eventType", default=None)

    payload: Optional[EventMarketDataKlineResponsePayload] = None
