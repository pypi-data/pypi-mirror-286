# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cadenza_sdk import Cadenza, AsyncCadenza
from tests.utils import assert_matches_type
from cadenza_sdk.types.event import Event

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvent:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_new(self, client: Cadenza) -> None:
        event = client.event.new(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(Event, event, path=["response"])

    @parametrize
    def test_method_new_with_all_params(self, client: Cadenza) -> None:
        event = client.event.new(
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
        assert_matches_type(Event, event, path=["response"])

    @parametrize
    def test_raw_response_new(self, client: Cadenza) -> None:
        response = client.event.with_raw_response.new(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(Event, event, path=["response"])

    @parametrize
    def test_streaming_response_new(self, client: Cadenza) -> None:
        with client.event.with_streaming_response.new(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(Event, event, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEvent:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_new(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.new(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(Event, event, path=["response"])

    @parametrize
    async def test_method_new_with_all_params(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.new(
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
        assert_matches_type(Event, event, path=["response"])

    @parametrize
    async def test_raw_response_new(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.with_raw_response.new(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(Event, event, path=["response"])

    @parametrize
    async def test_streaming_response_new(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.with_streaming_response.new(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(Event, event, path=["response"])

        assert cast(Any, response.is_closed) is True
