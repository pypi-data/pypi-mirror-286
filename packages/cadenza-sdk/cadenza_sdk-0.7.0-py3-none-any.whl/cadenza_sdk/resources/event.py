# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import (
    event_drop_copy_order_params,
    event_drop_copy_quote_params,
    event_market_data_kline_params,
    event_drop_copy_portfolio_params,
    event_market_data_order_book_params,
)
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
from ..types.trading.order_param import OrderParam
from ..types.trading.quote_param import QuoteParam
from ..types.market.orderbook_param import OrderbookParam
from ..types.event_drop_copy_order_response import EventDropCopyOrderResponse
from ..types.event_drop_copy_quote_response import EventDropCopyQuoteResponse
from ..types.event_market_data_kline_response import EventMarketDataKlineResponse
from ..types.exchange_account_portfolio_param import ExchangeAccountPortfolioParam
from ..types.event_drop_copy_portfolio_response import EventDropCopyPortfolioResponse
from ..types.event_market_data_order_book_response import EventMarketDataOrderBookResponse

__all__ = ["EventResource", "AsyncEventResource"]


class EventResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EventResourceWithRawResponse:
        return EventResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EventResourceWithStreamingResponse:
        return EventResourceWithStreamingResponse(self)

    def drop_copy_order(
        self,
        *,
        event_id: str,
        event_type: Literal[
            "cadenza.dropCopy.order",
            "cadenza.task.placeOrderRequestAck",
            "cadenza.task.cancelOrderRequestAck",
            "cadenza.dropCopy.quote",
            "cadenza.dropCopy.portfolio",
            "cadenza.marketData.orderBook",
            "cadenza.marketData.kline",
        ],
        timestamp: int,
        payload: OrderParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventDropCopyOrderResponse:
        """
        PubSub event handler placeholder for order event

        Args:
          event_id: A unique identifier for the event.

          timestamp: Unix timestamp in milliseconds when the event was generated.

          source: The source system or module that generated the event.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/webhook/pubsub/dropCopy/order",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                event_drop_copy_order_params.EventDropCopyOrderParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventDropCopyOrderResponse,
        )

    def drop_copy_portfolio(
        self,
        *,
        event_id: str,
        event_type: Literal[
            "cadenza.dropCopy.portfolio",
            "cadenza.task.placeOrderRequestAck",
            "cadenza.task.cancelOrderRequestAck",
            "cadenza.dropCopy.quote",
            "cadenza.dropCopy.order",
            "cadenza.marketData.orderBook",
            "cadenza.marketData.kline",
        ],
        timestamp: int,
        payload: ExchangeAccountPortfolioParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventDropCopyPortfolioResponse:
        """
        PubSub event handler placeholder for portfolio event

        Args:
          event_id: A unique identifier for the event.

          timestamp: Unix timestamp in milliseconds when the event was generated.

          source: The source system or module that generated the event.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/webhook/pubsub/dropCopy/portfolio",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                event_drop_copy_portfolio_params.EventDropCopyPortfolioParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventDropCopyPortfolioResponse,
        )

    def drop_copy_quote(
        self,
        *,
        event_id: str,
        event_type: Literal[
            "cadenza.dropCopy.quote",
            "cadenza.task.placeOrderRequestAck",
            "cadenza.task.cancelOrderRequestAck",
            "cadenza.dropCopy.order",
            "cadenza.dropCopy.portfolio",
            "cadenza.marketData.orderBook",
            "cadenza.marketData.kline",
        ],
        timestamp: int,
        payload: QuoteParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventDropCopyQuoteResponse:
        """
        PubSub event handler placeholder for quote event

        Args:
          event_id: A unique identifier for the event.

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
            cast_to=EventDropCopyQuoteResponse,
        )

    def market_data_kline(
        self,
        *,
        event_id: str,
        event_type: Literal[
            "cadenza.marketData.kline",
            "cadenza.task.placeOrderRequestAck",
            "cadenza.task.cancelOrderRequestAck",
            "cadenza.dropCopy.quote",
            "cadenza.dropCopy.order",
            "cadenza.dropCopy.portfolio",
            "cadenza.marketData.orderBook",
        ],
        timestamp: int,
        payload: event_market_data_kline_params.Payload | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventMarketDataKlineResponse:
        """
        PubSub event handler placeholder for kline event

        Args:
          event_id: A unique identifier for the event.

          timestamp: Unix timestamp in milliseconds when the event was generated.

          source: The source system or module that generated the event.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/webhook/pubsub/marketData/kline",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                event_market_data_kline_params.EventMarketDataKlineParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventMarketDataKlineResponse,
        )

    def market_data_order_book(
        self,
        *,
        event_id: str,
        event_type: Literal[
            "cadenza.marketData.orderBook",
            "cadenza.task.placeOrderRequestAck",
            "cadenza.task.cancelOrderRequestAck",
            "cadenza.dropCopy.quote",
            "cadenza.dropCopy.order",
            "cadenza.dropCopy.portfolio",
            "cadenza.marketData.kline",
        ],
        timestamp: int,
        payload: OrderbookParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventMarketDataOrderBookResponse:
        """
        PubSub event handler placeholder for order book event

        Args:
          event_id: A unique identifier for the event.

          timestamp: Unix timestamp in milliseconds when the event was generated.

          source: The source system or module that generated the event.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/webhook/pubsub/marketData/orderBook",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                event_market_data_order_book_params.EventMarketDataOrderBookParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventMarketDataOrderBookResponse,
        )


class AsyncEventResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEventResourceWithRawResponse:
        return AsyncEventResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEventResourceWithStreamingResponse:
        return AsyncEventResourceWithStreamingResponse(self)

    async def drop_copy_order(
        self,
        *,
        event_id: str,
        event_type: Literal[
            "cadenza.dropCopy.order",
            "cadenza.task.placeOrderRequestAck",
            "cadenza.task.cancelOrderRequestAck",
            "cadenza.dropCopy.quote",
            "cadenza.dropCopy.portfolio",
            "cadenza.marketData.orderBook",
            "cadenza.marketData.kline",
        ],
        timestamp: int,
        payload: OrderParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventDropCopyOrderResponse:
        """
        PubSub event handler placeholder for order event

        Args:
          event_id: A unique identifier for the event.

          timestamp: Unix timestamp in milliseconds when the event was generated.

          source: The source system or module that generated the event.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/webhook/pubsub/dropCopy/order",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                event_drop_copy_order_params.EventDropCopyOrderParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventDropCopyOrderResponse,
        )

    async def drop_copy_portfolio(
        self,
        *,
        event_id: str,
        event_type: Literal[
            "cadenza.dropCopy.portfolio",
            "cadenza.task.placeOrderRequestAck",
            "cadenza.task.cancelOrderRequestAck",
            "cadenza.dropCopy.quote",
            "cadenza.dropCopy.order",
            "cadenza.marketData.orderBook",
            "cadenza.marketData.kline",
        ],
        timestamp: int,
        payload: ExchangeAccountPortfolioParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventDropCopyPortfolioResponse:
        """
        PubSub event handler placeholder for portfolio event

        Args:
          event_id: A unique identifier for the event.

          timestamp: Unix timestamp in milliseconds when the event was generated.

          source: The source system or module that generated the event.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/webhook/pubsub/dropCopy/portfolio",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                event_drop_copy_portfolio_params.EventDropCopyPortfolioParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventDropCopyPortfolioResponse,
        )

    async def drop_copy_quote(
        self,
        *,
        event_id: str,
        event_type: Literal[
            "cadenza.dropCopy.quote",
            "cadenza.task.placeOrderRequestAck",
            "cadenza.task.cancelOrderRequestAck",
            "cadenza.dropCopy.order",
            "cadenza.dropCopy.portfolio",
            "cadenza.marketData.orderBook",
            "cadenza.marketData.kline",
        ],
        timestamp: int,
        payload: QuoteParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventDropCopyQuoteResponse:
        """
        PubSub event handler placeholder for quote event

        Args:
          event_id: A unique identifier for the event.

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
            cast_to=EventDropCopyQuoteResponse,
        )

    async def market_data_kline(
        self,
        *,
        event_id: str,
        event_type: Literal[
            "cadenza.marketData.kline",
            "cadenza.task.placeOrderRequestAck",
            "cadenza.task.cancelOrderRequestAck",
            "cadenza.dropCopy.quote",
            "cadenza.dropCopy.order",
            "cadenza.dropCopy.portfolio",
            "cadenza.marketData.orderBook",
        ],
        timestamp: int,
        payload: event_market_data_kline_params.Payload | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventMarketDataKlineResponse:
        """
        PubSub event handler placeholder for kline event

        Args:
          event_id: A unique identifier for the event.

          timestamp: Unix timestamp in milliseconds when the event was generated.

          source: The source system or module that generated the event.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/webhook/pubsub/marketData/kline",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                event_market_data_kline_params.EventMarketDataKlineParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventMarketDataKlineResponse,
        )

    async def market_data_order_book(
        self,
        *,
        event_id: str,
        event_type: Literal[
            "cadenza.marketData.orderBook",
            "cadenza.task.placeOrderRequestAck",
            "cadenza.task.cancelOrderRequestAck",
            "cadenza.dropCopy.quote",
            "cadenza.dropCopy.order",
            "cadenza.dropCopy.portfolio",
            "cadenza.marketData.kline",
        ],
        timestamp: int,
        payload: OrderbookParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventMarketDataOrderBookResponse:
        """
        PubSub event handler placeholder for order book event

        Args:
          event_id: A unique identifier for the event.

          timestamp: Unix timestamp in milliseconds when the event was generated.

          source: The source system or module that generated the event.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/webhook/pubsub/marketData/orderBook",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                event_market_data_order_book_params.EventMarketDataOrderBookParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventMarketDataOrderBookResponse,
        )


class EventResourceWithRawResponse:
    def __init__(self, event: EventResource) -> None:
        self._event = event

        self.drop_copy_order = to_raw_response_wrapper(
            event.drop_copy_order,
        )
        self.drop_copy_portfolio = to_raw_response_wrapper(
            event.drop_copy_portfolio,
        )
        self.drop_copy_quote = to_raw_response_wrapper(
            event.drop_copy_quote,
        )
        self.market_data_kline = to_raw_response_wrapper(
            event.market_data_kline,
        )
        self.market_data_order_book = to_raw_response_wrapper(
            event.market_data_order_book,
        )


class AsyncEventResourceWithRawResponse:
    def __init__(self, event: AsyncEventResource) -> None:
        self._event = event

        self.drop_copy_order = async_to_raw_response_wrapper(
            event.drop_copy_order,
        )
        self.drop_copy_portfolio = async_to_raw_response_wrapper(
            event.drop_copy_portfolio,
        )
        self.drop_copy_quote = async_to_raw_response_wrapper(
            event.drop_copy_quote,
        )
        self.market_data_kline = async_to_raw_response_wrapper(
            event.market_data_kline,
        )
        self.market_data_order_book = async_to_raw_response_wrapper(
            event.market_data_order_book,
        )


class EventResourceWithStreamingResponse:
    def __init__(self, event: EventResource) -> None:
        self._event = event

        self.drop_copy_order = to_streamed_response_wrapper(
            event.drop_copy_order,
        )
        self.drop_copy_portfolio = to_streamed_response_wrapper(
            event.drop_copy_portfolio,
        )
        self.drop_copy_quote = to_streamed_response_wrapper(
            event.drop_copy_quote,
        )
        self.market_data_kline = to_streamed_response_wrapper(
            event.market_data_kline,
        )
        self.market_data_order_book = to_streamed_response_wrapper(
            event.market_data_order_book,
        )


class AsyncEventResourceWithStreamingResponse:
    def __init__(self, event: AsyncEventResource) -> None:
        self._event = event

        self.drop_copy_order = async_to_streamed_response_wrapper(
            event.drop_copy_order,
        )
        self.drop_copy_portfolio = async_to_streamed_response_wrapper(
            event.drop_copy_portfolio,
        )
        self.drop_copy_quote = async_to_streamed_response_wrapper(
            event.drop_copy_quote,
        )
        self.market_data_kline = async_to_streamed_response_wrapper(
            event.market_data_kline,
        )
        self.market_data_order_book = async_to_streamed_response_wrapper(
            event.market_data_order_book,
        )
