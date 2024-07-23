# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import webhook_pubsub_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options

__all__ = ["WebhookResource", "AsyncWebhookResource"]


class WebhookResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> WebhookResourceWithRawResponse:
        return WebhookResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WebhookResourceWithStreamingResponse:
        return WebhookResourceWithStreamingResponse(self)

    def pubsub(
        self,
        *,
        event_id: str,
        event_type: str,
        payload: webhook_pubsub_params.Payload,
        timestamp: int,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        PubSub Event Handler

        Args:
          event_id: A unique identifier for the event.

          event_type: The type of the event (e.g., order, executionReport, portfolio, orderBook).

          payload: The actual data of the event, which varies based on the event type.

          timestamp: Unix timestamp in milliseconds when the event was generated.

          source: The source system or module that generated the event.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/webhook/pubsub",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "payload": payload,
                    "timestamp": timestamp,
                    "source": source,
                },
                webhook_pubsub_params.WebhookPubsubParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncWebhookResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncWebhookResourceWithRawResponse:
        return AsyncWebhookResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWebhookResourceWithStreamingResponse:
        return AsyncWebhookResourceWithStreamingResponse(self)

    async def pubsub(
        self,
        *,
        event_id: str,
        event_type: str,
        payload: webhook_pubsub_params.Payload,
        timestamp: int,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        PubSub Event Handler

        Args:
          event_id: A unique identifier for the event.

          event_type: The type of the event (e.g., order, executionReport, portfolio, orderBook).

          payload: The actual data of the event, which varies based on the event type.

          timestamp: Unix timestamp in milliseconds when the event was generated.

          source: The source system or module that generated the event.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/webhook/pubsub",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "payload": payload,
                    "timestamp": timestamp,
                    "source": source,
                },
                webhook_pubsub_params.WebhookPubsubParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class WebhookResourceWithRawResponse:
    def __init__(self, webhook: WebhookResource) -> None:
        self._webhook = webhook

        self.pubsub = to_raw_response_wrapper(
            webhook.pubsub,
        )


class AsyncWebhookResourceWithRawResponse:
    def __init__(self, webhook: AsyncWebhookResource) -> None:
        self._webhook = webhook

        self.pubsub = async_to_raw_response_wrapper(
            webhook.pubsub,
        )


class WebhookResourceWithStreamingResponse:
    def __init__(self, webhook: WebhookResource) -> None:
        self._webhook = webhook

        self.pubsub = to_streamed_response_wrapper(
            webhook.pubsub,
        )


class AsyncWebhookResourceWithStreamingResponse:
    def __init__(self, webhook: AsyncWebhookResource) -> None:
        self._webhook = webhook

        self.pubsub = async_to_streamed_response_wrapper(
            webhook.pubsub,
        )
