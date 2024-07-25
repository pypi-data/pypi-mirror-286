# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cadenza_sdk import Cadenza, AsyncCadenza
from tests.utils import assert_matches_type
from cadenza_sdk.types import (
    GenericEvent,
    DropCopyOrder,
    DropCopyQuote,
    MarketDataKline,
    DropCopyPortfolio,
    MarketDataOrderBook,
    TaskQuoteRequestAck,
    DropCopyExecutionReport,
    TaskPlaceOrderRequestAck,
    TaskCancelOrderRequestAck,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvent:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_drop_copy_execution_report(self, client: Cadenza) -> None:
        event = client.event.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyExecutionReport, event, path=["response"])

    @parametrize
    def test_method_drop_copy_execution_report_with_all_params(self, client: Cadenza) -> None:
        event = client.event.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={
                "cl_ord_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "base_currency": "BTC",
                "quote_currency": "USDT",
                "route_policy": "PRIORITY",
                "order": {
                    "cost": 0,
                    "created_at": 1703052635110,
                    "exchange_type": "BINANCE",
                    "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "filled": 0,
                    "order_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "order_side": "BUY",
                    "order_type": "MARKET",
                    "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "price": 0,
                    "quantity": 0,
                    "quote_quantity": 0,
                    "status": "SUBMITTED",
                    "symbol": "BTC/USDT",
                    "time_in_force": "DAY",
                    "updated_at": 1703052635111,
                    "user_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "fee": 0,
                    "fee_currency": "USDT",
                    "tenant_id": "tenantId",
                },
                "filled": 1,
                "cost": 42859.99,
                "fees": [
                    {
                        "asset": "asset",
                        "quantity": 0,
                    },
                    {
                        "asset": "asset",
                        "quantity": 0,
                    },
                    {
                        "asset": "asset",
                        "quantity": 0,
                    },
                ],
                "status": "SUBMITTED",
                "created_at": 1632933600000,
                "updated_at": 1632933600000,
                "executions": [
                    {
                        "cost": 0,
                        "created_at": 1703052635110,
                        "exchange_type": "BINANCE",
                        "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "filled": 0,
                        "order_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "order_side": "BUY",
                        "order_type": "MARKET",
                        "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "price": 0,
                        "quantity": 0,
                        "quote_quantity": 0,
                        "status": "SUBMITTED",
                        "symbol": "BTC/USDT",
                        "time_in_force": "DAY",
                        "updated_at": 1703052635111,
                        "user_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "fee": 0,
                        "fee_currency": "USDT",
                        "tenant_id": "tenantId",
                    },
                    {
                        "cost": 0,
                        "created_at": 1703052635110,
                        "exchange_type": "BINANCE",
                        "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "filled": 0,
                        "order_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "order_side": "BUY",
                        "order_type": "MARKET",
                        "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "price": 0,
                        "quantity": 0,
                        "quote_quantity": 0,
                        "status": "SUBMITTED",
                        "symbol": "BTC/USDT",
                        "time_in_force": "DAY",
                        "updated_at": 1703052635111,
                        "user_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "fee": 0,
                        "fee_currency": "USDT",
                        "tenant_id": "tenantId",
                    },
                    {
                        "cost": 0,
                        "created_at": 1703052635110,
                        "exchange_type": "BINANCE",
                        "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "filled": 0,
                        "order_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "order_side": "BUY",
                        "order_type": "MARKET",
                        "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "price": 0,
                        "quantity": 0,
                        "quote_quantity": 0,
                        "status": "SUBMITTED",
                        "symbol": "BTC/USDT",
                        "time_in_force": "DAY",
                        "updated_at": 1703052635111,
                        "user_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "fee": 0,
                        "fee_currency": "USDT",
                        "tenant_id": "tenantId",
                    },
                ],
            },
            source="source",
        )
        assert_matches_type(DropCopyExecutionReport, event, path=["response"])

    @parametrize
    def test_raw_response_drop_copy_execution_report(self, client: Cadenza) -> None:
        response = client.event.with_raw_response.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(DropCopyExecutionReport, event, path=["response"])

    @parametrize
    def test_streaming_response_drop_copy_execution_report(self, client: Cadenza) -> None:
        with client.event.with_streaming_response.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(DropCopyExecutionReport, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_drop_copy_order(self, client: Cadenza) -> None:
        event = client.event.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyOrder, event, path=["response"])

    @parametrize
    def test_method_drop_copy_order_with_all_params(self, client: Cadenza) -> None:
        event = client.event.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={
                "cost": 0,
                "created_at": 1703052635110,
                "exchange_type": "BINANCE",
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "filled": 0,
                "order_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "order_side": "BUY",
                "order_type": "MARKET",
                "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "price": 0,
                "quantity": 0,
                "quote_quantity": 0,
                "status": "SUBMITTED",
                "symbol": "BTC/USDT",
                "time_in_force": "DAY",
                "updated_at": 1703052635111,
                "user_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "fee": 0,
                "fee_currency": "USDT",
                "tenant_id": "tenantId",
            },
            source="source",
        )
        assert_matches_type(DropCopyOrder, event, path=["response"])

    @parametrize
    def test_raw_response_drop_copy_order(self, client: Cadenza) -> None:
        response = client.event.with_raw_response.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(DropCopyOrder, event, path=["response"])

    @parametrize
    def test_streaming_response_drop_copy_order(self, client: Cadenza) -> None:
        with client.event.with_streaming_response.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(DropCopyOrder, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_drop_copy_portfolio(self, client: Cadenza) -> None:
        event = client.event.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyPortfolio, event, path=["response"])

    @parametrize
    def test_method_drop_copy_portfolio_with_all_params(self, client: Cadenza) -> None:
        event = client.event.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={
                "payload": {
                    "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "exchange_type": "BINANCE",
                    "balances": [
                        {
                            "asset": "BTC",
                            "free": 1,
                            "locked": 0,
                            "total": 1,
                        },
                        {
                            "asset": "BTC",
                            "free": 1,
                            "locked": 0,
                            "total": 1,
                        },
                        {
                            "asset": "BTC",
                            "free": 1,
                            "locked": 0,
                            "total": 1,
                        },
                    ],
                    "positions": [
                        {
                            "amount": 0,
                            "cost": 0,
                            "entry_price": 0,
                            "position_side": "LONG",
                            "status": "OPEN",
                            "symbol": "BTC/USDT",
                        },
                        {
                            "amount": 0,
                            "cost": 0,
                            "entry_price": 0,
                            "position_side": "LONG",
                            "status": "OPEN",
                            "symbol": "BTC/USDT",
                        },
                        {
                            "amount": 0,
                            "cost": 0,
                            "entry_price": 0,
                            "position_side": "LONG",
                            "status": "OPEN",
                            "symbol": "BTC/USDT",
                        },
                    ],
                    "credit": {
                        "exchange_account_id": "018e41a1-cebc-7b49-a729-ae2c1c41e297",
                        "exchange_type": "BINANCE",
                        "account_type": "SPOT",
                        "currency": "USDT",
                        "leverage": 1,
                        "credit": 10000,
                        "margin": 5000,
                        "margin_loan": 3000,
                        "margin_requirement": 1500,
                        "margin_usage": 0.5,
                        "margin_level": 0.89,
                        "risk_exposure": 5677517.76,
                        "max_risk_exposure": 5000000,
                        "risk_exposure_rate": 0.89,
                    },
                    "updated_at": 1632933600000,
                }
            },
            source="source",
        )
        assert_matches_type(DropCopyPortfolio, event, path=["response"])

    @parametrize
    def test_raw_response_drop_copy_portfolio(self, client: Cadenza) -> None:
        response = client.event.with_raw_response.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(DropCopyPortfolio, event, path=["response"])

    @parametrize
    def test_streaming_response_drop_copy_portfolio(self, client: Cadenza) -> None:
        with client.event.with_streaming_response.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(DropCopyPortfolio, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_drop_copy_quote(self, client: Cadenza) -> None:
        event = client.event.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyQuote, event, path=["response"])

    @parametrize
    def test_method_drop_copy_quote_with_all_params(self, client: Cadenza) -> None:
        event = client.event.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={
                "quote_request_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "base_currency": "BTC",
                "quote_currency": "USDT",
                "ask_price": 42859.99,
                "ask_quantity": 1,
                "bid_price": 42859.71,
                "bid_quantity": 1,
                "timestamp": 1632933600000,
                "valid_until": 1632933600000,
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "exchange_type": "BINANCE",
            },
            source="source",
        )
        assert_matches_type(DropCopyQuote, event, path=["response"])

    @parametrize
    def test_raw_response_drop_copy_quote(self, client: Cadenza) -> None:
        response = client.event.with_raw_response.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(DropCopyQuote, event, path=["response"])

    @parametrize
    def test_streaming_response_drop_copy_quote(self, client: Cadenza) -> None:
        with client.event.with_streaming_response.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(DropCopyQuote, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_market_data_kline(self, client: Cadenza) -> None:
        event = client.event.market_data_kline(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(MarketDataKline, event, path=["response"])

    @parametrize
    def test_method_market_data_kline_with_all_params(self, client: Cadenza) -> None:
        event = client.event.market_data_kline(
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
        assert_matches_type(MarketDataKline, event, path=["response"])

    @parametrize
    def test_raw_response_market_data_kline(self, client: Cadenza) -> None:
        response = client.event.with_raw_response.market_data_kline(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(MarketDataKline, event, path=["response"])

    @parametrize
    def test_streaming_response_market_data_kline(self, client: Cadenza) -> None:
        with client.event.with_streaming_response.market_data_kline(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(MarketDataKline, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_market_data_order_book(self, client: Cadenza) -> None:
        event = client.event.market_data_order_book(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(MarketDataOrderBook, event, path=["response"])

    @parametrize
    def test_method_market_data_order_book_with_all_params(self, client: Cadenza) -> None:
        event = client.event.market_data_order_book(
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
        assert_matches_type(MarketDataOrderBook, event, path=["response"])

    @parametrize
    def test_raw_response_market_data_order_book(self, client: Cadenza) -> None:
        response = client.event.with_raw_response.market_data_order_book(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(MarketDataOrderBook, event, path=["response"])

    @parametrize
    def test_streaming_response_market_data_order_book(self, client: Cadenza) -> None:
        with client.event.with_streaming_response.market_data_order_book(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(MarketDataOrderBook, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_new(self, client: Cadenza) -> None:
        event = client.event.new(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(GenericEvent, event, path=["response"])

    @parametrize
    def test_method_new_with_all_params(self, client: Cadenza) -> None:
        event = client.event.new(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={
                "base_currency": "baseCurrency",
                "quote_currency": "quoteCurrency",
                "order_side": "orderSide",
                "quantity": 0,
                "quote_quantity": 0,
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            },
            source="source",
        )
        assert_matches_type(GenericEvent, event, path=["response"])

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
        assert_matches_type(GenericEvent, event, path=["response"])

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
            assert_matches_type(GenericEvent, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_task_cancel_order_request_ack(self, client: Cadenza) -> None:
        event = client.event.task_cancel_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(TaskCancelOrderRequestAck, event, path=["response"])

    @parametrize
    def test_method_task_cancel_order_request_ack_with_all_params(self, client: Cadenza) -> None:
        event = client.event.task_cancel_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={"order_id": "orderId"},
            source="source",
        )
        assert_matches_type(TaskCancelOrderRequestAck, event, path=["response"])

    @parametrize
    def test_raw_response_task_cancel_order_request_ack(self, client: Cadenza) -> None:
        response = client.event.with_raw_response.task_cancel_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(TaskCancelOrderRequestAck, event, path=["response"])

    @parametrize
    def test_streaming_response_task_cancel_order_request_ack(self, client: Cadenza) -> None:
        with client.event.with_streaming_response.task_cancel_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(TaskCancelOrderRequestAck, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_task_place_order_request_ack(self, client: Cadenza) -> None:
        event = client.event.task_place_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(TaskPlaceOrderRequestAck, event, path=["response"])

    @parametrize
    def test_method_task_place_order_request_ack_with_all_params(self, client: Cadenza) -> None:
        event = client.event.task_place_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={
                "quote_request_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "leverage": 0,
                "order_side": "BUY",
                "order_type": "MARKET",
                "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "price": 0,
                "price_slippage_tolerance": 0,
                "quantity": 0,
                "quote_quantity": 0,
                "symbol": "BTC/USDT",
                "time_in_force": "DAY",
                "route_policy": "PRIORITY",
                "priority": ["exchange_account_id_1", "exchange_account_id_2", "exchange_account_id_3"],
                "quote_id": "quoteId",
                "tenant_id": "tenantId",
            },
            source="source",
        )
        assert_matches_type(TaskPlaceOrderRequestAck, event, path=["response"])

    @parametrize
    def test_raw_response_task_place_order_request_ack(self, client: Cadenza) -> None:
        response = client.event.with_raw_response.task_place_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(TaskPlaceOrderRequestAck, event, path=["response"])

    @parametrize
    def test_streaming_response_task_place_order_request_ack(self, client: Cadenza) -> None:
        with client.event.with_streaming_response.task_place_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(TaskPlaceOrderRequestAck, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_task_quote_request_ack(self, client: Cadenza) -> None:
        event = client.event.task_quote_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(TaskQuoteRequestAck, event, path=["response"])

    @parametrize
    def test_method_task_quote_request_ack_with_all_params(self, client: Cadenza) -> None:
        event = client.event.task_quote_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={
                "base_currency": "baseCurrency",
                "quote_currency": "quoteCurrency",
                "order_side": "orderSide",
                "quantity": 0,
                "quote_quantity": 0,
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            },
            source="source",
        )
        assert_matches_type(TaskQuoteRequestAck, event, path=["response"])

    @parametrize
    def test_raw_response_task_quote_request_ack(self, client: Cadenza) -> None:
        response = client.event.with_raw_response.task_quote_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(TaskQuoteRequestAck, event, path=["response"])

    @parametrize
    def test_streaming_response_task_quote_request_ack(self, client: Cadenza) -> None:
        with client.event.with_streaming_response.task_quote_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(TaskQuoteRequestAck, event, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEvent:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_drop_copy_execution_report(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyExecutionReport, event, path=["response"])

    @parametrize
    async def test_method_drop_copy_execution_report_with_all_params(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={
                "cl_ord_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "base_currency": "BTC",
                "quote_currency": "USDT",
                "route_policy": "PRIORITY",
                "order": {
                    "cost": 0,
                    "created_at": 1703052635110,
                    "exchange_type": "BINANCE",
                    "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "filled": 0,
                    "order_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "order_side": "BUY",
                    "order_type": "MARKET",
                    "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "price": 0,
                    "quantity": 0,
                    "quote_quantity": 0,
                    "status": "SUBMITTED",
                    "symbol": "BTC/USDT",
                    "time_in_force": "DAY",
                    "updated_at": 1703052635111,
                    "user_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "fee": 0,
                    "fee_currency": "USDT",
                    "tenant_id": "tenantId",
                },
                "filled": 1,
                "cost": 42859.99,
                "fees": [
                    {
                        "asset": "asset",
                        "quantity": 0,
                    },
                    {
                        "asset": "asset",
                        "quantity": 0,
                    },
                    {
                        "asset": "asset",
                        "quantity": 0,
                    },
                ],
                "status": "SUBMITTED",
                "created_at": 1632933600000,
                "updated_at": 1632933600000,
                "executions": [
                    {
                        "cost": 0,
                        "created_at": 1703052635110,
                        "exchange_type": "BINANCE",
                        "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "filled": 0,
                        "order_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "order_side": "BUY",
                        "order_type": "MARKET",
                        "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "price": 0,
                        "quantity": 0,
                        "quote_quantity": 0,
                        "status": "SUBMITTED",
                        "symbol": "BTC/USDT",
                        "time_in_force": "DAY",
                        "updated_at": 1703052635111,
                        "user_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "fee": 0,
                        "fee_currency": "USDT",
                        "tenant_id": "tenantId",
                    },
                    {
                        "cost": 0,
                        "created_at": 1703052635110,
                        "exchange_type": "BINANCE",
                        "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "filled": 0,
                        "order_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "order_side": "BUY",
                        "order_type": "MARKET",
                        "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "price": 0,
                        "quantity": 0,
                        "quote_quantity": 0,
                        "status": "SUBMITTED",
                        "symbol": "BTC/USDT",
                        "time_in_force": "DAY",
                        "updated_at": 1703052635111,
                        "user_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "fee": 0,
                        "fee_currency": "USDT",
                        "tenant_id": "tenantId",
                    },
                    {
                        "cost": 0,
                        "created_at": 1703052635110,
                        "exchange_type": "BINANCE",
                        "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "filled": 0,
                        "order_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "order_side": "BUY",
                        "order_type": "MARKET",
                        "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "price": 0,
                        "quantity": 0,
                        "quote_quantity": 0,
                        "status": "SUBMITTED",
                        "symbol": "BTC/USDT",
                        "time_in_force": "DAY",
                        "updated_at": 1703052635111,
                        "user_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "fee": 0,
                        "fee_currency": "USDT",
                        "tenant_id": "tenantId",
                    },
                ],
            },
            source="source",
        )
        assert_matches_type(DropCopyExecutionReport, event, path=["response"])

    @parametrize
    async def test_raw_response_drop_copy_execution_report(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.with_raw_response.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(DropCopyExecutionReport, event, path=["response"])

    @parametrize
    async def test_streaming_response_drop_copy_execution_report(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.with_streaming_response.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(DropCopyExecutionReport, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_drop_copy_order(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyOrder, event, path=["response"])

    @parametrize
    async def test_method_drop_copy_order_with_all_params(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={
                "cost": 0,
                "created_at": 1703052635110,
                "exchange_type": "BINANCE",
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "filled": 0,
                "order_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "order_side": "BUY",
                "order_type": "MARKET",
                "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "price": 0,
                "quantity": 0,
                "quote_quantity": 0,
                "status": "SUBMITTED",
                "symbol": "BTC/USDT",
                "time_in_force": "DAY",
                "updated_at": 1703052635111,
                "user_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "fee": 0,
                "fee_currency": "USDT",
                "tenant_id": "tenantId",
            },
            source="source",
        )
        assert_matches_type(DropCopyOrder, event, path=["response"])

    @parametrize
    async def test_raw_response_drop_copy_order(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.with_raw_response.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(DropCopyOrder, event, path=["response"])

    @parametrize
    async def test_streaming_response_drop_copy_order(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.with_streaming_response.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(DropCopyOrder, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_drop_copy_portfolio(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyPortfolio, event, path=["response"])

    @parametrize
    async def test_method_drop_copy_portfolio_with_all_params(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={
                "payload": {
                    "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "exchange_type": "BINANCE",
                    "balances": [
                        {
                            "asset": "BTC",
                            "free": 1,
                            "locked": 0,
                            "total": 1,
                        },
                        {
                            "asset": "BTC",
                            "free": 1,
                            "locked": 0,
                            "total": 1,
                        },
                        {
                            "asset": "BTC",
                            "free": 1,
                            "locked": 0,
                            "total": 1,
                        },
                    ],
                    "positions": [
                        {
                            "amount": 0,
                            "cost": 0,
                            "entry_price": 0,
                            "position_side": "LONG",
                            "status": "OPEN",
                            "symbol": "BTC/USDT",
                        },
                        {
                            "amount": 0,
                            "cost": 0,
                            "entry_price": 0,
                            "position_side": "LONG",
                            "status": "OPEN",
                            "symbol": "BTC/USDT",
                        },
                        {
                            "amount": 0,
                            "cost": 0,
                            "entry_price": 0,
                            "position_side": "LONG",
                            "status": "OPEN",
                            "symbol": "BTC/USDT",
                        },
                    ],
                    "credit": {
                        "exchange_account_id": "018e41a1-cebc-7b49-a729-ae2c1c41e297",
                        "exchange_type": "BINANCE",
                        "account_type": "SPOT",
                        "currency": "USDT",
                        "leverage": 1,
                        "credit": 10000,
                        "margin": 5000,
                        "margin_loan": 3000,
                        "margin_requirement": 1500,
                        "margin_usage": 0.5,
                        "margin_level": 0.89,
                        "risk_exposure": 5677517.76,
                        "max_risk_exposure": 5000000,
                        "risk_exposure_rate": 0.89,
                    },
                    "updated_at": 1632933600000,
                }
            },
            source="source",
        )
        assert_matches_type(DropCopyPortfolio, event, path=["response"])

    @parametrize
    async def test_raw_response_drop_copy_portfolio(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.with_raw_response.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(DropCopyPortfolio, event, path=["response"])

    @parametrize
    async def test_streaming_response_drop_copy_portfolio(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.with_streaming_response.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(DropCopyPortfolio, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_drop_copy_quote(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyQuote, event, path=["response"])

    @parametrize
    async def test_method_drop_copy_quote_with_all_params(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={
                "quote_request_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "base_currency": "BTC",
                "quote_currency": "USDT",
                "ask_price": 42859.99,
                "ask_quantity": 1,
                "bid_price": 42859.71,
                "bid_quantity": 1,
                "timestamp": 1632933600000,
                "valid_until": 1632933600000,
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "exchange_type": "BINANCE",
            },
            source="source",
        )
        assert_matches_type(DropCopyQuote, event, path=["response"])

    @parametrize
    async def test_raw_response_drop_copy_quote(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.with_raw_response.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(DropCopyQuote, event, path=["response"])

    @parametrize
    async def test_streaming_response_drop_copy_quote(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.with_streaming_response.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(DropCopyQuote, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_market_data_kline(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.market_data_kline(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(MarketDataKline, event, path=["response"])

    @parametrize
    async def test_method_market_data_kline_with_all_params(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.market_data_kline(
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
        assert_matches_type(MarketDataKline, event, path=["response"])

    @parametrize
    async def test_raw_response_market_data_kline(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.with_raw_response.market_data_kline(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(MarketDataKline, event, path=["response"])

    @parametrize
    async def test_streaming_response_market_data_kline(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.with_streaming_response.market_data_kline(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(MarketDataKline, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_market_data_order_book(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.market_data_order_book(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(MarketDataOrderBook, event, path=["response"])

    @parametrize
    async def test_method_market_data_order_book_with_all_params(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.market_data_order_book(
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
        assert_matches_type(MarketDataOrderBook, event, path=["response"])

    @parametrize
    async def test_raw_response_market_data_order_book(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.with_raw_response.market_data_order_book(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(MarketDataOrderBook, event, path=["response"])

    @parametrize
    async def test_streaming_response_market_data_order_book(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.with_streaming_response.market_data_order_book(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(MarketDataOrderBook, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_new(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.new(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(GenericEvent, event, path=["response"])

    @parametrize
    async def test_method_new_with_all_params(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.new(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={
                "base_currency": "baseCurrency",
                "quote_currency": "quoteCurrency",
                "order_side": "orderSide",
                "quantity": 0,
                "quote_quantity": 0,
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            },
            source="source",
        )
        assert_matches_type(GenericEvent, event, path=["response"])

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
        assert_matches_type(GenericEvent, event, path=["response"])

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
            assert_matches_type(GenericEvent, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_task_cancel_order_request_ack(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.task_cancel_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(TaskCancelOrderRequestAck, event, path=["response"])

    @parametrize
    async def test_method_task_cancel_order_request_ack_with_all_params(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.task_cancel_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={"order_id": "orderId"},
            source="source",
        )
        assert_matches_type(TaskCancelOrderRequestAck, event, path=["response"])

    @parametrize
    async def test_raw_response_task_cancel_order_request_ack(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.with_raw_response.task_cancel_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(TaskCancelOrderRequestAck, event, path=["response"])

    @parametrize
    async def test_streaming_response_task_cancel_order_request_ack(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.with_streaming_response.task_cancel_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(TaskCancelOrderRequestAck, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_task_place_order_request_ack(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.task_place_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(TaskPlaceOrderRequestAck, event, path=["response"])

    @parametrize
    async def test_method_task_place_order_request_ack_with_all_params(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.task_place_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={
                "quote_request_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "leverage": 0,
                "order_side": "BUY",
                "order_type": "MARKET",
                "position_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "price": 0,
                "price_slippage_tolerance": 0,
                "quantity": 0,
                "quote_quantity": 0,
                "symbol": "BTC/USDT",
                "time_in_force": "DAY",
                "route_policy": "PRIORITY",
                "priority": ["exchange_account_id_1", "exchange_account_id_2", "exchange_account_id_3"],
                "quote_id": "quoteId",
                "tenant_id": "tenantId",
            },
            source="source",
        )
        assert_matches_type(TaskPlaceOrderRequestAck, event, path=["response"])

    @parametrize
    async def test_raw_response_task_place_order_request_ack(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.with_raw_response.task_place_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(TaskPlaceOrderRequestAck, event, path=["response"])

    @parametrize
    async def test_streaming_response_task_place_order_request_ack(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.with_streaming_response.task_place_order_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(TaskPlaceOrderRequestAck, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_task_quote_request_ack(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.task_quote_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(TaskQuoteRequestAck, event, path=["response"])

    @parametrize
    async def test_method_task_quote_request_ack_with_all_params(self, async_client: AsyncCadenza) -> None:
        event = await async_client.event.task_quote_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={
                "base_currency": "baseCurrency",
                "quote_currency": "quoteCurrency",
                "order_side": "orderSide",
                "quantity": 0,
                "quote_quantity": 0,
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            },
            source="source",
        )
        assert_matches_type(TaskQuoteRequestAck, event, path=["response"])

    @parametrize
    async def test_raw_response_task_quote_request_ack(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.with_raw_response.task_quote_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(TaskQuoteRequestAck, event, path=["response"])

    @parametrize
    async def test_streaming_response_task_quote_request_ack(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.with_streaming_response.task_quote_request_ack(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(TaskQuoteRequestAck, event, path=["response"])

        assert cast(Any, response.is_closed) is True
