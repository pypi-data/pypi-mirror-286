# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.webhook.cloud_scheduler_update_portfolio_routine_response import (
    CloudSchedulerUpdatePortfolioRoutineResponse,
)

__all__ = ["CloudSchedulerResource", "AsyncCloudSchedulerResource"]


class CloudSchedulerResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CloudSchedulerResourceWithRawResponse:
        return CloudSchedulerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CloudSchedulerResourceWithStreamingResponse:
        return CloudSchedulerResourceWithStreamingResponse(self)

    def update_portfolio_routine(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CloudSchedulerUpdatePortfolioRoutineResponse:
        """Cloud scheduler update portfolio routine task"""
        return self._post(
            "/api/v2/webhook/cloudScheduler/updatePortfolioRoutine",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudSchedulerUpdatePortfolioRoutineResponse,
        )


class AsyncCloudSchedulerResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCloudSchedulerResourceWithRawResponse:
        return AsyncCloudSchedulerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCloudSchedulerResourceWithStreamingResponse:
        return AsyncCloudSchedulerResourceWithStreamingResponse(self)

    async def update_portfolio_routine(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CloudSchedulerUpdatePortfolioRoutineResponse:
        """Cloud scheduler update portfolio routine task"""
        return await self._post(
            "/api/v2/webhook/cloudScheduler/updatePortfolioRoutine",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CloudSchedulerUpdatePortfolioRoutineResponse,
        )


class CloudSchedulerResourceWithRawResponse:
    def __init__(self, cloud_scheduler: CloudSchedulerResource) -> None:
        self._cloud_scheduler = cloud_scheduler

        self.update_portfolio_routine = to_raw_response_wrapper(
            cloud_scheduler.update_portfolio_routine,
        )


class AsyncCloudSchedulerResourceWithRawResponse:
    def __init__(self, cloud_scheduler: AsyncCloudSchedulerResource) -> None:
        self._cloud_scheduler = cloud_scheduler

        self.update_portfolio_routine = async_to_raw_response_wrapper(
            cloud_scheduler.update_portfolio_routine,
        )


class CloudSchedulerResourceWithStreamingResponse:
    def __init__(self, cloud_scheduler: CloudSchedulerResource) -> None:
        self._cloud_scheduler = cloud_scheduler

        self.update_portfolio_routine = to_streamed_response_wrapper(
            cloud_scheduler.update_portfolio_routine,
        )


class AsyncCloudSchedulerResourceWithStreamingResponse:
    def __init__(self, cloud_scheduler: AsyncCloudSchedulerResource) -> None:
        self._cloud_scheduler = cloud_scheduler

        self.update_portfolio_routine = async_to_streamed_response_wrapper(
            cloud_scheduler.update_portfolio_routine,
        )
