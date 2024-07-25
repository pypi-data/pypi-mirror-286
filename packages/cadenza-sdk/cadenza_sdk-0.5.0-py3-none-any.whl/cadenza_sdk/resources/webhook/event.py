# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.webhook import event_drop_copy_quote_params
from ...types.trading.quote_param import QuoteParam
from ...types.webhook.drop_copy_quote import DropCopyQuote

__all__ = ["EventResource", "AsyncEventResource"]


class EventResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EventResourceWithRawResponse:
        return EventResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EventResourceWithStreamingResponse:
        return EventResourceWithStreamingResponse(self)

    def drop_copy_quote(
        self,
        *,
        event_id: str,
        event_type: str,
        timestamp: int,
        payload: QuoteParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DropCopyQuote:
        """
        PubSub event handler placeholder for quote event

        Args:
          event_id: A unique identifier for the event.

          event_type: The type of the event (e.g., order, executionReport, portfolio, orderBook).

          timestamp: Unix timestamp in milliseconds when the event was generated.

          source: The source system or module that generated the event.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/webhook/pubsub/dropCopy/quote",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                event_drop_copy_quote_params.EventDropCopyQuoteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DropCopyQuote,
        )


class AsyncEventResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEventResourceWithRawResponse:
        return AsyncEventResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEventResourceWithStreamingResponse:
        return AsyncEventResourceWithStreamingResponse(self)

    async def drop_copy_quote(
        self,
        *,
        event_id: str,
        event_type: str,
        timestamp: int,
        payload: QuoteParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DropCopyQuote:
        """
        PubSub event handler placeholder for quote event

        Args:
          event_id: A unique identifier for the event.

          event_type: The type of the event (e.g., order, executionReport, portfolio, orderBook).

          timestamp: Unix timestamp in milliseconds when the event was generated.

          source: The source system or module that generated the event.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/webhook/pubsub/dropCopy/quote",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                event_drop_copy_quote_params.EventDropCopyQuoteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DropCopyQuote,
        )


class EventResourceWithRawResponse:
    def __init__(self, event: EventResource) -> None:
        self._event = event

        self.drop_copy_quote = to_raw_response_wrapper(
            event.drop_copy_quote,
        )


class AsyncEventResourceWithRawResponse:
    def __init__(self, event: AsyncEventResource) -> None:
        self._event = event

        self.drop_copy_quote = async_to_raw_response_wrapper(
            event.drop_copy_quote,
        )


class EventResourceWithStreamingResponse:
    def __init__(self, event: EventResource) -> None:
        self._event = event

        self.drop_copy_quote = to_streamed_response_wrapper(
            event.drop_copy_quote,
        )


class AsyncEventResourceWithStreamingResponse:
    def __init__(self, event: AsyncEventResource) -> None:
        self._event = event

        self.drop_copy_quote = async_to_streamed_response_wrapper(
            event.drop_copy_quote,
        )
