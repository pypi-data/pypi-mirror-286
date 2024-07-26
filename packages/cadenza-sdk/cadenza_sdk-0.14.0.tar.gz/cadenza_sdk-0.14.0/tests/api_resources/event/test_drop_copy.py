# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cadenza_sdk import Cadenza, AsyncCadenza
from tests.utils import assert_matches_type
from cadenza_sdk.types.event import (
    DropCopyOrder,
    DropCopyQuote,
    DropCopyPortfolio,
    DropCopyExecutionReport,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDropCopy:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_drop_copy_execution_report(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyExecutionReport, drop_copy, path=["response"])

    @parametrize
    def test_method_drop_copy_execution_report_with_all_params(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_execution_report(
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
        assert_matches_type(DropCopyExecutionReport, drop_copy, path=["response"])

    @parametrize
    def test_raw_response_drop_copy_execution_report(self, client: Cadenza) -> None:
        response = client.event.drop_copy.with_raw_response.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = response.parse()
        assert_matches_type(DropCopyExecutionReport, drop_copy, path=["response"])

    @parametrize
    def test_streaming_response_drop_copy_execution_report(self, client: Cadenza) -> None:
        with client.event.drop_copy.with_streaming_response.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = response.parse()
            assert_matches_type(DropCopyExecutionReport, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_drop_copy_order(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyOrder, drop_copy, path=["response"])

    @parametrize
    def test_method_drop_copy_order_with_all_params(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_order(
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
        assert_matches_type(DropCopyOrder, drop_copy, path=["response"])

    @parametrize
    def test_raw_response_drop_copy_order(self, client: Cadenza) -> None:
        response = client.event.drop_copy.with_raw_response.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = response.parse()
        assert_matches_type(DropCopyOrder, drop_copy, path=["response"])

    @parametrize
    def test_streaming_response_drop_copy_order(self, client: Cadenza) -> None:
        with client.event.drop_copy.with_streaming_response.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = response.parse()
            assert_matches_type(DropCopyOrder, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_drop_copy_portfolio(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyPortfolio, drop_copy, path=["response"])

    @parametrize
    def test_method_drop_copy_portfolio_with_all_params(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "exchange_type": "BINANCE",
                "balances": [
                    {
                        "asset": "BTC",
                        "free": 1,
                        "locked": 0,
                        "borrowed": 3,
                        "net": -2,
                        "total": 1,
                    },
                    {
                        "asset": "BTC",
                        "free": 1,
                        "locked": 0,
                        "borrowed": 3,
                        "net": -2,
                        "total": 1,
                    },
                    {
                        "asset": "BTC",
                        "free": 1,
                        "locked": 0,
                        "borrowed": 3,
                        "net": -2,
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
            },
            source="source",
        )
        assert_matches_type(DropCopyPortfolio, drop_copy, path=["response"])

    @parametrize
    def test_raw_response_drop_copy_portfolio(self, client: Cadenza) -> None:
        response = client.event.drop_copy.with_raw_response.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = response.parse()
        assert_matches_type(DropCopyPortfolio, drop_copy, path=["response"])

    @parametrize
    def test_streaming_response_drop_copy_portfolio(self, client: Cadenza) -> None:
        with client.event.drop_copy.with_streaming_response.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = response.parse()
            assert_matches_type(DropCopyPortfolio, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_drop_copy_quote(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyQuote, drop_copy, path=["response"])

    @parametrize
    def test_method_drop_copy_quote_with_all_params(self, client: Cadenza) -> None:
        drop_copy = client.event.drop_copy.drop_copy_quote(
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
                "created_at": 1632933600000,
                "valid_until": 1632933600000,
                "expired_at": 1632933600000,
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "exchange_type": "BINANCE",
            },
            source="source",
        )
        assert_matches_type(DropCopyQuote, drop_copy, path=["response"])

    @parametrize
    def test_raw_response_drop_copy_quote(self, client: Cadenza) -> None:
        response = client.event.drop_copy.with_raw_response.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = response.parse()
        assert_matches_type(DropCopyQuote, drop_copy, path=["response"])

    @parametrize
    def test_streaming_response_drop_copy_quote(self, client: Cadenza) -> None:
        with client.event.drop_copy.with_streaming_response.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = response.parse()
            assert_matches_type(DropCopyQuote, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDropCopy:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_drop_copy_execution_report(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyExecutionReport, drop_copy, path=["response"])

    @parametrize
    async def test_method_drop_copy_execution_report_with_all_params(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_execution_report(
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
        assert_matches_type(DropCopyExecutionReport, drop_copy, path=["response"])

    @parametrize
    async def test_raw_response_drop_copy_execution_report(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.drop_copy.with_raw_response.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = await response.parse()
        assert_matches_type(DropCopyExecutionReport, drop_copy, path=["response"])

    @parametrize
    async def test_streaming_response_drop_copy_execution_report(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.drop_copy.with_streaming_response.drop_copy_execution_report(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = await response.parse()
            assert_matches_type(DropCopyExecutionReport, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_drop_copy_order(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyOrder, drop_copy, path=["response"])

    @parametrize
    async def test_method_drop_copy_order_with_all_params(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_order(
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
        assert_matches_type(DropCopyOrder, drop_copy, path=["response"])

    @parametrize
    async def test_raw_response_drop_copy_order(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.drop_copy.with_raw_response.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = await response.parse()
        assert_matches_type(DropCopyOrder, drop_copy, path=["response"])

    @parametrize
    async def test_streaming_response_drop_copy_order(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.drop_copy.with_streaming_response.drop_copy_order(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = await response.parse()
            assert_matches_type(DropCopyOrder, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_drop_copy_portfolio(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyPortfolio, drop_copy, path=["response"])

    @parametrize
    async def test_method_drop_copy_portfolio_with_all_params(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
            payload={
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "exchange_type": "BINANCE",
                "balances": [
                    {
                        "asset": "BTC",
                        "free": 1,
                        "locked": 0,
                        "borrowed": 3,
                        "net": -2,
                        "total": 1,
                    },
                    {
                        "asset": "BTC",
                        "free": 1,
                        "locked": 0,
                        "borrowed": 3,
                        "net": -2,
                        "total": 1,
                    },
                    {
                        "asset": "BTC",
                        "free": 1,
                        "locked": 0,
                        "borrowed": 3,
                        "net": -2,
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
            },
            source="source",
        )
        assert_matches_type(DropCopyPortfolio, drop_copy, path=["response"])

    @parametrize
    async def test_raw_response_drop_copy_portfolio(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.drop_copy.with_raw_response.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = await response.parse()
        assert_matches_type(DropCopyPortfolio, drop_copy, path=["response"])

    @parametrize
    async def test_streaming_response_drop_copy_portfolio(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.drop_copy.with_streaming_response.drop_copy_portfolio(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = await response.parse()
            assert_matches_type(DropCopyPortfolio, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_drop_copy_quote(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )
        assert_matches_type(DropCopyQuote, drop_copy, path=["response"])

    @parametrize
    async def test_method_drop_copy_quote_with_all_params(self, async_client: AsyncCadenza) -> None:
        drop_copy = await async_client.event.drop_copy.drop_copy_quote(
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
                "created_at": 1632933600000,
                "valid_until": 1632933600000,
                "expired_at": 1632933600000,
                "exchange_account_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "exchange_type": "BINANCE",
            },
            source="source",
        )
        assert_matches_type(DropCopyQuote, drop_copy, path=["response"])

    @parametrize
    async def test_raw_response_drop_copy_quote(self, async_client: AsyncCadenza) -> None:
        response = await async_client.event.drop_copy.with_raw_response.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        drop_copy = await response.parse()
        assert_matches_type(DropCopyQuote, drop_copy, path=["response"])

    @parametrize
    async def test_streaming_response_drop_copy_quote(self, async_client: AsyncCadenza) -> None:
        async with async_client.event.drop_copy.with_streaming_response.drop_copy_quote(
            event_id="eventId",
            event_type="cadenza.task.quoteRequestAck",
            timestamp=1632933600000,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            drop_copy = await response.parse()
            assert_matches_type(DropCopyQuote, drop_copy, path=["response"])

        assert cast(Any, response.is_closed) is True
