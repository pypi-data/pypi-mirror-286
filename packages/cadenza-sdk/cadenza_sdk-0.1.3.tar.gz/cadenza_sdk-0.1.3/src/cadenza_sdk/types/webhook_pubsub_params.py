# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .market.ohlcv_param import OhlcvParam
from .trading.order_param import OrderParam
from .market.orderbook_param import OrderbookParam
from .exchange_account_credit_param import ExchangeAccountCreditParam
from .trading.execution_report_param import ExecutionReportParam
from .trading.quote_with_order_candidates_param import QuoteWithOrderCandidatesParam

__all__ = [
    "WebhookPubsubParams",
    "Payload",
    "PayloadQuoteRequest",
    "PayloadPlaceOrderRequest",
    "PayloadCancelOrderRequest",
    "PayloadExchangeAccountPortfolio",
    "PayloadExchangeAccountPortfolioPayload",
    "PayloadExchangeAccountPortfolioPayloadBalance",
    "PayloadExchangeAccountPortfolioPayloadPosition",
    "PayloadKline",
]


class WebhookPubsubParams(TypedDict, total=False):
    event_id: Required[Annotated[str, PropertyInfo(alias="eventId")]]
    """A unique identifier for the event."""

    event_type: Required[Annotated[str, PropertyInfo(alias="eventType")]]
    """The type of the event (e.g., order, executionReport, portfolio, orderBook)."""

    payload: Required[Payload]
    """The actual data of the event, which varies based on the event type."""

    timestamp: Required[int]
    """Unix timestamp in milliseconds when the event was generated."""

    source: str
    """The source system or module that generated the event."""


class PayloadQuoteRequest(TypedDict, total=False):
    base_currency: Required[Annotated[str, PropertyInfo(alias="baseCurrency")]]
    """Base currency is the currency you want to buy or sell"""

    order_side: Required[Annotated[str, PropertyInfo(alias="orderSide")]]
    """Order side, BUY or SELL"""

    quote_currency: Required[Annotated[str, PropertyInfo(alias="quoteCurrency")]]
    """
    Quote currency is the currency you want to pay or receive, and the price of the
    base currency is quoted in the quote currency
    """

    exchange_account_id: Annotated[str, PropertyInfo(alias="exchangeAccountId")]
    """The identifier for the exchange account"""

    quantity: float
    """Amount of the base currency"""

    quote_quantity: Annotated[float, PropertyInfo(alias="quoteQuantity")]
    """Amount of the quote currency"""


class PayloadPlaceOrderRequest(TypedDict, total=False):
    exchange_account_id: Annotated[str, PropertyInfo(alias="exchangeAccountId")]
    """Exchange account ID"""

    leverage: int
    """Levarage"""

    order_side: Annotated[Literal["BUY", "SELL"], PropertyInfo(alias="orderSide")]
    """Order side"""

    order_type: Annotated[
        Literal["MARKET", "LIMIT", "STOP_LOSS", "STOP_LOSS_LIMIT", "TAKE_PROFIT", "TAKE_PROFIT_LIMIT", "QUOTED"],
        PropertyInfo(alias="orderType"),
    ]
    """Order type"""

    position_id: Annotated[str, PropertyInfo(alias="positionId")]
    """Position ID for closing position in margin trading"""

    price: float
    """Price"""

    price_slippage_tolerance: Annotated[float, PropertyInfo(alias="priceSlippageTolerance")]
    """Price slippage tolerance, range: [0, 0.1] with 2 decimal places"""

    priority: List[str]
    """Priority list of exchange account ID in descending order"""

    quantity: float
    """Quantity.

    One of quantity or quoteQuantity must be provided. If both is provided, only
    quantity will be used.
    """

    quote_id: Annotated[str, PropertyInfo(alias="quoteId")]
    """Quote ID used by exchange for RFQ, e.g.

    WINTERMUTE need this field to execute QUOTED order
    """

    quote_quantity: Annotated[float, PropertyInfo(alias="quoteQuantity")]
    """Quote Quantity"""

    quote_request_id: Annotated[str, PropertyInfo(alias="quoteRequestId")]
    """Quote request ID"""

    route_policy: Annotated[Literal["PRIORITY", "QUOTE"], PropertyInfo(alias="routePolicy")]
    """Route policy.

    For PRIORITY, the order request will be routed to the exchange account with the
    highest priority. For QUOTE, the system will execute the execution plan based on
    the quote. Order request with route policy QUOTE will only accept two
    parameters, quoteRequestId and priceSlippageTolerance
    """

    symbol: str
    """Symbol"""

    tenant_id: Annotated[str, PropertyInfo(alias="tenantId")]
    """Tenant ID"""

    time_in_force: Annotated[
        Literal["DAY", "GTC", "GTX", "GTD", "OPG", "CLS", "IOC", "FOK", "GFA", "GFS", "GTM", "MOO", "MOC", "EXT"],
        PropertyInfo(alias="timeInForce"),
    ]
    """Time in force"""


class PayloadCancelOrderRequest(TypedDict, total=False):
    order_id: Required[Annotated[str, PropertyInfo(alias="orderId")]]
    """Order ID"""


class PayloadExchangeAccountPortfolioPayloadBalance(TypedDict, total=False):
    asset: Required[str]
    """Asset"""

    free: Required[float]
    """Free balance"""

    locked: Required[float]
    """Locked balance"""

    total: Required[float]
    """Total balance"""


class PayloadExchangeAccountPortfolioPayloadPosition(TypedDict, total=False):
    amount: Required[float]
    """Amount"""

    position_side: Required[Annotated[Literal["LONG", "SHORT"], PropertyInfo(alias="positionSide")]]
    """Position side"""

    status: Required[Literal["OPEN"]]
    """Status"""

    symbol: Required[str]
    """Symbol"""

    cost: float
    """Cost"""

    entry_price: Annotated[float, PropertyInfo(alias="entryPrice")]
    """Entry price"""


class PayloadExchangeAccountPortfolioPayload(TypedDict, total=False):
    balances: Required[Iterable[PayloadExchangeAccountPortfolioPayloadBalance]]

    credit: Required[ExchangeAccountCreditParam]
    """Exchange Account Credit Info"""

    exchange_account_id: Required[Annotated[str, PropertyInfo(alias="exchangeAccountId")]]
    """The unique identifier for the account."""

    exchange_type: Required[
        Annotated[
            Literal["BINANCE", "BINANCE_MARGIN", "B2C2", "WINTERMUTE", "BLOCKFILLS", "STONEX"],
            PropertyInfo(alias="exchangeType"),
        ]
    ]
    """Exchange type"""

    positions: Required[Iterable[PayloadExchangeAccountPortfolioPayloadPosition]]

    updated_at: Required[Annotated[int, PropertyInfo(alias="updatedAt")]]
    """The timestamp when the portfolio information was updated."""


class PayloadExchangeAccountPortfolio(TypedDict, total=False):
    payload: PayloadExchangeAccountPortfolioPayload


class PayloadKline(TypedDict, total=False):
    candles: Iterable[OhlcvParam]

    exchange_account_id: Annotated[str, PropertyInfo(alias="exchangeAccountId")]
    """The unique identifier for the account."""

    exchange_type: Annotated[
        Literal["BINANCE", "BINANCE_MARGIN", "B2C2", "WINTERMUTE", "BLOCKFILLS", "STONEX"],
        PropertyInfo(alias="exchangeType"),
    ]
    """Exchange type"""

    interval: Literal["1s", "1m", "5m", "15m", "30m", "1h", "2h", "1d", "1w"]

    symbol: str


Payload = Union[
    PayloadQuoteRequest,
    PayloadPlaceOrderRequest,
    PayloadCancelOrderRequest,
    QuoteWithOrderCandidatesParam,
    OrderParam,
    ExecutionReportParam,
    PayloadExchangeAccountPortfolio,
    OrderbookParam,
    PayloadKline,
]
