# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cadenza_sdk import Cadenza, AsyncCadenza
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestWebhook:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_pubsub(self, client: Cadenza) -> None:
        webhook = client.webhook.pubsub(
            event_id="eventId",
            event_type="eventType",
            payload={
                "base_currency": "baseCurrency",
                "quote_currency": "quoteCurrency",
                "order_side": "orderSide",
            },
            timestamp=1632933600000,
        )
        assert_matches_type(object, webhook, path=["response"])

    @parametrize
    def test_method_pubsub_with_all_params(self, client: Cadenza) -> None:
        webhook = client.webhook.pubsub(
            event_id="eventId",
            event_type="eventType",
            payload={
                "base_currency": "baseCurrency",
                "quote_currency": "quoteCurrency",
                "order_side": "orderSide",
                "quantity": 0,
                "quote_quantity": 0,
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            },
            timestamp=1632933600000,
            source="source",
        )
        assert_matches_type(object, webhook, path=["response"])

    @parametrize
    def test_raw_response_pubsub(self, client: Cadenza) -> None:
        response = client.webhook.with_raw_response.pubsub(
            event_id="eventId",
            event_type="eventType",
            payload={
                "base_currency": "baseCurrency",
                "quote_currency": "quoteCurrency",
                "order_side": "orderSide",
            },
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert_matches_type(object, webhook, path=["response"])

    @parametrize
    def test_streaming_response_pubsub(self, client: Cadenza) -> None:
        with client.webhook.with_streaming_response.pubsub(
            event_id="eventId",
            event_type="eventType",
            payload={
                "base_currency": "baseCurrency",
                "quote_currency": "quoteCurrency",
                "order_side": "orderSide",
            },
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert_matches_type(object, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncWebhook:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_pubsub(self, async_client: AsyncCadenza) -> None:
        webhook = await async_client.webhook.pubsub(
            event_id="eventId",
            event_type="eventType",
            payload={
                "base_currency": "baseCurrency",
                "quote_currency": "quoteCurrency",
                "order_side": "orderSide",
            },
            timestamp=1632933600000,
        )
        assert_matches_type(object, webhook, path=["response"])

    @parametrize
    async def test_method_pubsub_with_all_params(self, async_client: AsyncCadenza) -> None:
        webhook = await async_client.webhook.pubsub(
            event_id="eventId",
            event_type="eventType",
            payload={
                "base_currency": "baseCurrency",
                "quote_currency": "quoteCurrency",
                "order_side": "orderSide",
                "quantity": 0,
                "quote_quantity": 0,
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            },
            timestamp=1632933600000,
            source="source",
        )
        assert_matches_type(object, webhook, path=["response"])

    @parametrize
    async def test_raw_response_pubsub(self, async_client: AsyncCadenza) -> None:
        response = await async_client.webhook.with_raw_response.pubsub(
            event_id="eventId",
            event_type="eventType",
            payload={
                "base_currency": "baseCurrency",
                "quote_currency": "quoteCurrency",
                "order_side": "orderSide",
            },
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert_matches_type(object, webhook, path=["response"])

    @parametrize
    async def test_streaming_response_pubsub(self, async_client: AsyncCadenza) -> None:
        async with async_client.webhook.with_streaming_response.pubsub(
            event_id="eventId",
            event_type="eventType",
            payload={
                "base_currency": "baseCurrency",
                "quote_currency": "quoteCurrency",
                "order_side": "orderSide",
            },
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert_matches_type(object, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True
