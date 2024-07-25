# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cadenza_sdk import Cadenza, AsyncCadenza
from tests.utils import assert_matches_type
from cadenza_sdk.types.webhook import CloudSchedulerUpdatePortfolioRoutineResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCloudScheduler:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_update_portfolio_routine(self, client: Cadenza) -> None:
        cloud_scheduler = client.webhook.cloud_scheduler.update_portfolio_routine()
        assert_matches_type(CloudSchedulerUpdatePortfolioRoutineResponse, cloud_scheduler, path=["response"])

    @parametrize
    def test_raw_response_update_portfolio_routine(self, client: Cadenza) -> None:
        response = client.webhook.cloud_scheduler.with_raw_response.update_portfolio_routine()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        cloud_scheduler = response.parse()
        assert_matches_type(CloudSchedulerUpdatePortfolioRoutineResponse, cloud_scheduler, path=["response"])

    @parametrize
    def test_streaming_response_update_portfolio_routine(self, client: Cadenza) -> None:
        with client.webhook.cloud_scheduler.with_streaming_response.update_portfolio_routine() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            cloud_scheduler = response.parse()
            assert_matches_type(CloudSchedulerUpdatePortfolioRoutineResponse, cloud_scheduler, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncCloudScheduler:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_update_portfolio_routine(self, async_client: AsyncCadenza) -> None:
        cloud_scheduler = await async_client.webhook.cloud_scheduler.update_portfolio_routine()
        assert_matches_type(CloudSchedulerUpdatePortfolioRoutineResponse, cloud_scheduler, path=["response"])

    @parametrize
    async def test_raw_response_update_portfolio_routine(self, async_client: AsyncCadenza) -> None:
        response = await async_client.webhook.cloud_scheduler.with_raw_response.update_portfolio_routine()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        cloud_scheduler = await response.parse()
        assert_matches_type(CloudSchedulerUpdatePortfolioRoutineResponse, cloud_scheduler, path=["response"])

    @parametrize
    async def test_streaming_response_update_portfolio_routine(self, async_client: AsyncCadenza) -> None:
        async with async_client.webhook.cloud_scheduler.with_streaming_response.update_portfolio_routine() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            cloud_scheduler = await response.parse()
            assert_matches_type(CloudSchedulerUpdatePortfolioRoutineResponse, cloud_scheduler, path=["response"])

        assert cast(Any, response.is_closed) is True
