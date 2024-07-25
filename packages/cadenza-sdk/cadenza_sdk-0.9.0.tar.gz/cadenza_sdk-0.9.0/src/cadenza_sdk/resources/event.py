# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import (
    event_new_params,
    event_drop_copy_order_params,
    event_drop_copy_quote_params,
    event_market_data_kline_params,
    event_drop_copy_portfolio_params,
    event_market_data_order_book_params,
    event_task_quote_request_ack_params,
    event_drop_copy_execution_report_params,
    event_task_place_order_request_ack_params,
    event_task_cancel_order_request_ack_params,
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
from ..types.generic_event import GenericEvent
from ..types.drop_copy_order import DropCopyOrder
from ..types.drop_copy_quote import DropCopyQuote
from ..types.market_data_kline import MarketDataKline
from ..types.drop_copy_portfolio import DropCopyPortfolio
from ..types.trading.order_param import OrderParam
from ..types.trading.quote_param import QuoteParam
from ..types.market.orderbook_param import OrderbookParam
from ..types.market_data_order_book import MarketDataOrderBook
from ..types.task_quote_request_ack import TaskQuoteRequestAck
from ..types.drop_copy_execution_report import DropCopyExecutionReport
from ..types.trading.quote_request_param import QuoteRequestParam
from ..types.task_place_order_request_ack import TaskPlaceOrderRequestAck
from ..types.task_cancel_order_request_ack import TaskCancelOrderRequestAck
from ..types.trading.execution_report_param import ExecutionReportParam
from ..types.exchange_account_portfolio_param import ExchangeAccountPortfolioParam
from ..types.trading.place_order_request_param import PlaceOrderRequestParam
from ..types.trading.cancel_order_request_param import CancelOrderRequestParam

__all__ = ["EventResource", "AsyncEventResource"]


class EventResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EventResourceWithRawResponse:
        return EventResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EventResourceWithStreamingResponse:
        return EventResourceWithStreamingResponse(self)

    def drop_copy_execution_report(
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
        payload: ExecutionReportParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DropCopyExecutionReport:
        """
        PubSub event handler for execution report drop copy event

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
            "/api/v2/webhook/pubsub/dropCopy/executionReport",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                event_drop_copy_execution_report_params.EventDropCopyExecutionReportParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DropCopyExecutionReport,
        )

    def drop_copy_order(
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
        payload: OrderParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DropCopyOrder:
        """
        PubSub event handler placeholder for order event

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
            cast_to=DropCopyOrder,
        )

    def drop_copy_portfolio(
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
        payload: ExchangeAccountPortfolioParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DropCopyPortfolio:
        """
        PubSub event handler placeholder for portfolio event

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
            cast_to=DropCopyPortfolio,
        )

    def drop_copy_quote(
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

          event_type: Event Type

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
        payload: event_market_data_kline_params.Payload | NotGiven = NOT_GIVEN,
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
                event_market_data_kline_params.EventMarketDataKlineParams,
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
                event_market_data_order_book_params.EventMarketDataOrderBookParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MarketDataOrderBook,
        )

    def new(
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
        payload: event_new_params.Payload | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenericEvent:
        """
        PubSub event handler placeholder

        Args:
          event_id: A unique identifier for the event.

          event_type: Event Type

          timestamp: Unix timestamp in milliseconds when the event was generated.

          payload: The actual data of the event, which varies based on the event type.

          source: The source system or module that generated the event.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/webhook/pubsub/event",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                event_new_params.EventNewParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericEvent,
        )

    def task_cancel_order_request_ack(
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
        payload: CancelOrderRequestParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskCancelOrderRequestAck:
        """
        PubSub event handler placeholder for cancel order request acknowledgment event

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
            "/api/v2/webhook/pubsub/task/cancelOrderRequestAck",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                event_task_cancel_order_request_ack_params.EventTaskCancelOrderRequestAckParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskCancelOrderRequestAck,
        )

    def task_place_order_request_ack(
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
        payload: PlaceOrderRequestParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskPlaceOrderRequestAck:
        """
        PubSub event handler placeholder for place order request acknowledgment event

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
            "/api/v2/webhook/pubsub/task/placeOrderRequestAck",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                event_task_place_order_request_ack_params.EventTaskPlaceOrderRequestAckParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskPlaceOrderRequestAck,
        )

    def task_quote_request_ack(
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
        payload: QuoteRequestParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskQuoteRequestAck:
        """
        PubSub event handler placeholder for quote request acknowledgment event

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
            "/api/v2/webhook/pubsub/task/quoteRequestAck",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                event_task_quote_request_ack_params.EventTaskQuoteRequestAckParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskQuoteRequestAck,
        )


class AsyncEventResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEventResourceWithRawResponse:
        return AsyncEventResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEventResourceWithStreamingResponse:
        return AsyncEventResourceWithStreamingResponse(self)

    async def drop_copy_execution_report(
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
        payload: ExecutionReportParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DropCopyExecutionReport:
        """
        PubSub event handler for execution report drop copy event

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
            "/api/v2/webhook/pubsub/dropCopy/executionReport",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                event_drop_copy_execution_report_params.EventDropCopyExecutionReportParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DropCopyExecutionReport,
        )

    async def drop_copy_order(
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
        payload: OrderParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DropCopyOrder:
        """
        PubSub event handler placeholder for order event

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
            cast_to=DropCopyOrder,
        )

    async def drop_copy_portfolio(
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
        payload: ExchangeAccountPortfolioParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DropCopyPortfolio:
        """
        PubSub event handler placeholder for portfolio event

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
            cast_to=DropCopyPortfolio,
        )

    async def drop_copy_quote(
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

          event_type: Event Type

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
        payload: event_market_data_kline_params.Payload | NotGiven = NOT_GIVEN,
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
                event_market_data_kline_params.EventMarketDataKlineParams,
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
                event_market_data_order_book_params.EventMarketDataOrderBookParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MarketDataOrderBook,
        )

    async def new(
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
        payload: event_new_params.Payload | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GenericEvent:
        """
        PubSub event handler placeholder

        Args:
          event_id: A unique identifier for the event.

          event_type: Event Type

          timestamp: Unix timestamp in milliseconds when the event was generated.

          payload: The actual data of the event, which varies based on the event type.

          source: The source system or module that generated the event.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/webhook/pubsub/event",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                event_new_params.EventNewParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericEvent,
        )

    async def task_cancel_order_request_ack(
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
        payload: CancelOrderRequestParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskCancelOrderRequestAck:
        """
        PubSub event handler placeholder for cancel order request acknowledgment event

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
            "/api/v2/webhook/pubsub/task/cancelOrderRequestAck",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                event_task_cancel_order_request_ack_params.EventTaskCancelOrderRequestAckParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskCancelOrderRequestAck,
        )

    async def task_place_order_request_ack(
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
        payload: PlaceOrderRequestParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskPlaceOrderRequestAck:
        """
        PubSub event handler placeholder for place order request acknowledgment event

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
            "/api/v2/webhook/pubsub/task/placeOrderRequestAck",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                event_task_place_order_request_ack_params.EventTaskPlaceOrderRequestAckParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskPlaceOrderRequestAck,
        )

    async def task_quote_request_ack(
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
        payload: QuoteRequestParam | NotGiven = NOT_GIVEN,
        source: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskQuoteRequestAck:
        """
        PubSub event handler placeholder for quote request acknowledgment event

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
            "/api/v2/webhook/pubsub/task/quoteRequestAck",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "event_type": event_type,
                    "timestamp": timestamp,
                    "payload": payload,
                    "source": source,
                },
                event_task_quote_request_ack_params.EventTaskQuoteRequestAckParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskQuoteRequestAck,
        )


class EventResourceWithRawResponse:
    def __init__(self, event: EventResource) -> None:
        self._event = event

        self.drop_copy_execution_report = to_raw_response_wrapper(
            event.drop_copy_execution_report,
        )
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
        self.new = to_raw_response_wrapper(
            event.new,
        )
        self.task_cancel_order_request_ack = to_raw_response_wrapper(
            event.task_cancel_order_request_ack,
        )
        self.task_place_order_request_ack = to_raw_response_wrapper(
            event.task_place_order_request_ack,
        )
        self.task_quote_request_ack = to_raw_response_wrapper(
            event.task_quote_request_ack,
        )


class AsyncEventResourceWithRawResponse:
    def __init__(self, event: AsyncEventResource) -> None:
        self._event = event

        self.drop_copy_execution_report = async_to_raw_response_wrapper(
            event.drop_copy_execution_report,
        )
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
        self.new = async_to_raw_response_wrapper(
            event.new,
        )
        self.task_cancel_order_request_ack = async_to_raw_response_wrapper(
            event.task_cancel_order_request_ack,
        )
        self.task_place_order_request_ack = async_to_raw_response_wrapper(
            event.task_place_order_request_ack,
        )
        self.task_quote_request_ack = async_to_raw_response_wrapper(
            event.task_quote_request_ack,
        )


class EventResourceWithStreamingResponse:
    def __init__(self, event: EventResource) -> None:
        self._event = event

        self.drop_copy_execution_report = to_streamed_response_wrapper(
            event.drop_copy_execution_report,
        )
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
        self.new = to_streamed_response_wrapper(
            event.new,
        )
        self.task_cancel_order_request_ack = to_streamed_response_wrapper(
            event.task_cancel_order_request_ack,
        )
        self.task_place_order_request_ack = to_streamed_response_wrapper(
            event.task_place_order_request_ack,
        )
        self.task_quote_request_ack = to_streamed_response_wrapper(
            event.task_quote_request_ack,
        )


class AsyncEventResourceWithStreamingResponse:
    def __init__(self, event: AsyncEventResource) -> None:
        self._event = event

        self.drop_copy_execution_report = async_to_streamed_response_wrapper(
            event.drop_copy_execution_report,
        )
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
        self.new = async_to_streamed_response_wrapper(
            event.new,
        )
        self.task_cancel_order_request_ack = async_to_streamed_response_wrapper(
            event.task_cancel_order_request_ack,
        )
        self.task_place_order_request_ack = async_to_streamed_response_wrapper(
            event.task_place_order_request_ack,
        )
        self.task_quote_request_ack = async_to_streamed_response_wrapper(
            event.task_quote_request_ack,
        )
