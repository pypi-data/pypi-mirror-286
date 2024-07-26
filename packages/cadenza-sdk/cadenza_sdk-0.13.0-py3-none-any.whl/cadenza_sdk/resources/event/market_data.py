# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

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
from ...types.event import market_data_market_data_kline_params, market_data_market_data_order_book_params
from ..._base_client import make_request_options
from ...types.market.orderbook_param import OrderbookParam
from ...types.event.market_data_kline import MarketDataKline
from ...types.event.market_data_order_book import MarketDataOrderBook

__all__ = ["MarketDataResource", "AsyncMarketDataResource"]


class MarketDataResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MarketDataResourceWithRawResponse:
        return MarketDataResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MarketDataResourceWithStreamingResponse:
        return MarketDataResourceWithStreamingResponse(self)

    def market_data_kline(
        self,
        *,
        event_id: str,
        event_type: Literal[
            "cadenza.task.quoteRequestAck",
            "cadenza.task.placeOrderRequestAck",
            "cadenza.task.cancelOrderRequestAck",
            "cadenza.dropCopy.quote",
            "cadenza.dropCopy.order",
            "cadenza.dropCopy.portfolio",
            "cadenza.marketData.orderBook",
            "cadenza.marketData.kline",
        ],
        timestamp: int,
        payload: market_data_market_data_kline_params.Payload | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MarketDataKline:
        """
        PubSub event handler placeholder for kline event

        Args:
          event_id: A unique identifier for the event.

          event_type: Event Type

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
                market_data_market_data_kline_params.MarketDataMarketDataKlineParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MarketDataKline,
        )

    def market_data_order_book(
        self,
        *,
        event_id: str,
        event_type: Literal[
            "cadenza.task.quoteRequestAck",
            "cadenza.task.placeOrderRequestAck",
            "cadenza.task.cancelOrderRequestAck",
            "cadenza.dropCopy.quote",
            "cadenza.dropCopy.order",
            "cadenza.dropCopy.portfolio",
            "cadenza.marketData.orderBook",
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
    ) -> MarketDataOrderBook:
        """
        PubSub event handler placeholder for order book event

        Args:
          event_id: A unique identifier for the event.

          event_type: Event Type

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
                market_data_market_data_order_book_params.MarketDataMarketDataOrderBookParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MarketDataOrderBook,
        )


class AsyncMarketDataResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMarketDataResourceWithRawResponse:
        return AsyncMarketDataResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMarketDataResourceWithStreamingResponse:
        return AsyncMarketDataResourceWithStreamingResponse(self)

    async def market_data_kline(
        self,
        *,
        event_id: str,
        event_type: Literal[
            "cadenza.task.quoteRequestAck",
            "cadenza.task.placeOrderRequestAck",
            "cadenza.task.cancelOrderRequestAck",
            "cadenza.dropCopy.quote",
            "cadenza.dropCopy.order",
            "cadenza.dropCopy.portfolio",
            "cadenza.marketData.orderBook",
            "cadenza.marketData.kline",
        ],
        timestamp: int,
        payload: market_data_market_data_kline_params.Payload | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MarketDataKline:
        """
        PubSub event handler placeholder for kline event

        Args:
          event_id: A unique identifier for the event.

          event_type: Event Type

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
                market_data_market_data_kline_params.MarketDataMarketDataKlineParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MarketDataKline,
        )

    async def market_data_order_book(
        self,
        *,
        event_id: str,
        event_type: Literal[
            "cadenza.task.quoteRequestAck",
            "cadenza.task.placeOrderRequestAck",
            "cadenza.task.cancelOrderRequestAck",
            "cadenza.dropCopy.quote",
            "cadenza.dropCopy.order",
            "cadenza.dropCopy.portfolio",
            "cadenza.marketData.orderBook",
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
    ) -> MarketDataOrderBook:
        """
        PubSub event handler placeholder for order book event

        Args:
          event_id: A unique identifier for the event.

          event_type: Event Type

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
                market_data_market_data_order_book_params.MarketDataMarketDataOrderBookParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MarketDataOrderBook,
        )


class MarketDataResourceWithRawResponse:
    def __init__(self, market_data: MarketDataResource) -> None:
        self._market_data = market_data

        self.market_data_kline = to_raw_response_wrapper(
            market_data.market_data_kline,
        )
        self.market_data_order_book = to_raw_response_wrapper(
            market_data.market_data_order_book,
        )


class AsyncMarketDataResourceWithRawResponse:
    def __init__(self, market_data: AsyncMarketDataResource) -> None:
        self._market_data = market_data

        self.market_data_kline = async_to_raw_response_wrapper(
            market_data.market_data_kline,
        )
        self.market_data_order_book = async_to_raw_response_wrapper(
            market_data.market_data_order_book,
        )


class MarketDataResourceWithStreamingResponse:
    def __init__(self, market_data: MarketDataResource) -> None:
        self._market_data = market_data

        self.market_data_kline = to_streamed_response_wrapper(
            market_data.market_data_kline,
        )
        self.market_data_order_book = to_streamed_response_wrapper(
            market_data.market_data_order_book,
        )


class AsyncMarketDataResourceWithStreamingResponse:
    def __init__(self, market_data: AsyncMarketDataResource) -> None:
        self._market_data = market_data

        self.market_data_kline = async_to_streamed_response_wrapper(
            market_data.market_data_kline,
        )
        self.market_data_order_book = async_to_streamed_response_wrapper(
            market_data.market_data_order_book,
        )
