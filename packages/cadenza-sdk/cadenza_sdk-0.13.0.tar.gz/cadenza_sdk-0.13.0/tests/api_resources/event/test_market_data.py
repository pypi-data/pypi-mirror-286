# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cadenza_sdk import Cadenza, AsyncCadenza
from tests.utils import assert_matches_type
from cadenza_sdk.types.event import (
    MarketDataKline,
    MarketDataOrderBook,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMarketData:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_market_data_kline(self, client: Cadenza) -> None:
        market_data = client.event.market_data.market_data_kline(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(MarketDataKline, market_data, path=["response"])

    @parametrize
    def test_method_market_data_kline_with_all_params(self, client: Cadenza) -> None:
        market_data = client.event.market_data.market_data_kline(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "exchange_type": "BINANCE",
                "symbol": "symbol",
                "interval": "1s",
                "candles": [
                    {
                        "c": 0,
                        "h": 0,
                        "l": 0,
                        "o": 0,
                        "t": 0,
                        "v": 0,
                    },
                    {
                        "c": 0,
                        "h": 0,
                        "l": 0,
                        "o": 0,
                        "t": 0,
                        "v": 0,
                    },
                    {
                        "c": 0,
                        "h": 0,
                        "l": 0,
                        "o": 0,
                        "t": 0,
                        "v": 0,
                    },
                ],
            },
            source="source",
        )
        assert_matches_type(MarketDataKline, market_data, path=["response"])

    @parametrize
    def test_raw_response_market_data_kline(self, client: Cadenza) -> None:
        response = client.event.market_data.with_raw_response.market_data_kline(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        market_data = response.parse()
        assert_matches_type(MarketDataKline, market_data, path=["response"])

    @parametrize
    def test_streaming_response_market_data_kline(self, client: Cadenza) -> None:
        with client.event.market_data.with_streaming_response.market_data_kline(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            market_data = response.parse()
            assert_matches_type(MarketDataKline, market_data, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_market_data_order_book(self, client: Cadenza) -> None:
        market_data = client.event.market_data.market_data_order_book(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(MarketDataOrderBook, market_data, path=["response"])

    @parametrize
    def test_method_market_data_order_book_with_all_params(self, client: Cadenza) -> None:
        market_data = client.event.market_data.market_data_order_book(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={
                "asks": [[0, 0], [0, 0], [0, 0]],
                "bids": [[0, 0], [0, 0], [0, 0]],
                "exchange_type": "exchangeType",
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "symbol": "symbol",
                "level": 0,
            },
            source="source",
        )
        assert_matches_type(MarketDataOrderBook, market_data, path=["response"])

    @parametrize
    def test_raw_response_market_data_order_book(self, client: Cadenza) -> None:
        response = client.event.market_data.with_raw_response.market_data_order_book(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        market_data = response.parse()
        assert_matches_type(MarketDataOrderBook, market_data, path=["response"])

    @parametrize
    def test_streaming_response_market_data_order_book(self, client: Cadenza) -> None:
        with client.event.market_data.with_streaming_response.market_data_order_book(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            market_data = response.parse()
            assert_matches_type(MarketDataOrderBook, market_data, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncMarketData:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_market_data_kline(self, async_client: AsyncCadenza) -> None:
        market_data = await async_client.event.market_data.market_data_kline(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(MarketDataKline, market_data, path=["response"])

    @parametrize
    async def test_method_market_data_kline_with_all_params(self, async_client: AsyncCadenza) -> None:
        market_data = await async_client.event.market_data.market_data_kline(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "exchange_type": "BINANCE",
                "symbol": "symbol",
                "interval": "1s",
                "candles": [
                    {
                        "c": 0,
                        "h": 0,
                        "l": 0,
                        "o": 0,
                        "t": 0,
                        "v": 0,
                    },
                    {
                        "c": 0,
                        "h": 0,
                        "l": 0,
                        "o": 0,
                        "t": 0,
                        "v": 0,
                    },
                    {
                        "c": 0,
                        "h": 0,
                        "l": 0,
                        "o": 0,
                        "t": 0,
                        "v": 0,
                    },
                ],
            },
            source="source",
        )
        assert_matches_type(MarketDataKline, market_data, path=["response"])

    @parametrize
    async def test_raw_response_market_data_kline(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.market_data.with_raw_response.market_data_kline(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        market_data = await response.parse()
        assert_matches_type(MarketDataKline, market_data, path=["response"])

    @parametrize
    async def test_streaming_response_market_data_kline(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.market_data.with_streaming_response.market_data_kline(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            market_data = await response.parse()
            assert_matches_type(MarketDataKline, market_data, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_market_data_order_book(self, async_client: AsyncCadenza) -> None:
        market_data = await async_client.event.market_data.market_data_order_book(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(MarketDataOrderBook, market_data, path=["response"])

    @parametrize
    async def test_method_market_data_order_book_with_all_params(self, async_client: AsyncCadenza) -> None:
        market_data = await async_client.event.market_data.market_data_order_book(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={
                "asks": [[0, 0], [0, 0], [0, 0]],
                "bids": [[0, 0], [0, 0], [0, 0]],
                "exchange_type": "exchangeType",
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "symbol": "symbol",
                "level": 0,
            },
            source="source",
        )
        assert_matches_type(MarketDataOrderBook, market_data, path=["response"])

    @parametrize
    async def test_raw_response_market_data_order_book(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.market_data.with_raw_response.market_data_order_book(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        market_data = await response.parse()
        assert_matches_type(MarketDataOrderBook, market_data, path=["response"])

    @parametrize
    async def test_streaming_response_market_data_order_book(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.market_data.with_streaming_response.market_data_order_book(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            market_data = await response.parse()
            assert_matches_type(MarketDataOrderBook, market_data, path=["response"])

        assert cast(Any, response.is_closed) is True
