# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .market.ohlcv import Ohlcv
from .trading.order import Order
from .trading.quote import Quote
from .market.orderbook import Orderbook
from .exchange_account_credit import ExchangeAccountCredit
from .trading.execution_report import ExecutionReport

__all__ = [
    "Event",
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


class PayloadQuoteRequest(BaseModel):
    base_currency: str = FieldInfo(alias="baseCurrency")
    """Base currency is the currency you want to buy or sell"""

    order_side: str = FieldInfo(alias="orderSide")
    """Order side, BUY or SELL"""

    quote_currency: str = FieldInfo(alias="quoteCurrency")
    """
    Quote currency is the currency you want to pay or receive, and the price of the
    base currency is quoted in the quote currency
    """

    exchange_account_id: Optional[str] = FieldInfo(alias="exchangeAccountId", default=None)
    """The identifier for the exchange account"""

    quantity: Optional[float] = None
    """Amount of the base currency"""

    quote_quantity: Optional[float] = FieldInfo(alias="quoteQuantity", default=None)
    """Amount of the quote currency"""


class PayloadPlaceOrderRequest(BaseModel):
    exchange_account_id: Optional[str] = FieldInfo(alias="exchangeAccountId", default=None)
    """Exchange account ID"""

    leverage: Optional[int] = None
    """Levarage"""

    order_side: Optional[Literal["BUY", "SELL"]] = FieldInfo(alias="orderSide", default=None)
    """Order side"""

    order_type: Optional[
        Literal["MARKET", "LIMIT", "STOP_LOSS", "STOP_LOSS_LIMIT", "TAKE_PROFIT", "TAKE_PROFIT_LIMIT", "QUOTED"]
    ] = FieldInfo(alias="orderType", default=None)
    """Order type"""

    position_id: Optional[str] = FieldInfo(alias="positionId", default=None)
    """Position ID for closing position in margin trading"""

    price: Optional[float] = None
    """Price"""

    price_slippage_tolerance: Optional[float] = FieldInfo(alias="priceSlippageTolerance", default=None)
    """Price slippage tolerance, range: [0, 0.1] with 2 decimal places"""

    priority: Optional[List[str]] = None
    """Priority list of exchange account ID in descending order"""

    quantity: Optional[float] = None
    """Quantity.

    One of quantity or quoteQuantity must be provided. If both is provided, only
    quantity will be used.
    """

    quote_id: Optional[str] = FieldInfo(alias="quoteId", default=None)
    """Quote ID used by exchange for RFQ, e.g.

    WINTERMUTE need this field to execute QUOTED order
    """

    quote_quantity: Optional[float] = FieldInfo(alias="quoteQuantity", default=None)
    """Quote Quantity"""

    quote_request_id: Optional[str] = FieldInfo(alias="quoteRequestId", default=None)
    """Quote request ID"""

    route_policy: Optional[Literal["PRIORITY", "QUOTE"]] = FieldInfo(alias="routePolicy", default=None)
    """Route policy.

    For PRIORITY, the order request will be routed to the exchange account with the
    highest priority. For QUOTE, the system will execute the execution plan based on
    the quote. Order request with route policy QUOTE will only accept two
    parameters, quoteRequestId and priceSlippageTolerance
    """

    symbol: Optional[str] = None
    """Symbol"""

    tenant_id: Optional[str] = FieldInfo(alias="tenantId", default=None)
    """Tenant ID"""

    time_in_force: Optional[
        Literal["DAY", "GTC", "GTX", "GTD", "OPG", "CLS", "IOC", "FOK", "GFA", "GFS", "GTM", "MOO", "MOC", "EXT"]
    ] = FieldInfo(alias="timeInForce", default=None)
    """Time in force"""


class PayloadCancelOrderRequest(BaseModel):
    order_id: str = FieldInfo(alias="orderId")
    """Order ID"""


class PayloadExchangeAccountPortfolioPayloadBalance(BaseModel):
    asset: str
    """Asset"""

    free: float
    """Free balance"""

    locked: float
    """Locked balance"""

    total: float
    """Total balance"""


class PayloadExchangeAccountPortfolioPayloadPosition(BaseModel):
    amount: float
    """Amount"""

    position_side: Literal["LONG", "SHORT"] = FieldInfo(alias="positionSide")
    """Position side"""

    status: Literal["OPEN"]
    """Status"""

    symbol: str
    """Symbol"""

    cost: Optional[float] = None
    """Cost"""

    entry_price: Optional[float] = FieldInfo(alias="entryPrice", default=None)
    """Entry price"""


class PayloadExchangeAccountPortfolioPayload(BaseModel):
    balances: List[PayloadExchangeAccountPortfolioPayloadBalance]

    credit: ExchangeAccountCredit
    """Exchange Account Credit Info"""

    exchange_account_id: str = FieldInfo(alias="exchangeAccountId")
    """The unique identifier for the account."""

    exchange_type: Literal["BINANCE", "BINANCE_MARGIN", "B2C2", "WINTERMUTE", "BLOCKFILLS", "STONEX"] = FieldInfo(
        alias="exchangeType"
    )
    """Exchange type"""

    positions: List[PayloadExchangeAccountPortfolioPayloadPosition]

    updated_at: int = FieldInfo(alias="updatedAt")
    """The timestamp when the portfolio information was updated."""


class PayloadExchangeAccountPortfolio(BaseModel):
    payload: Optional[PayloadExchangeAccountPortfolioPayload] = None


class PayloadKline(BaseModel):
    candles: Optional[List[Ohlcv]] = None

    exchange_account_id: Optional[str] = FieldInfo(alias="exchangeAccountId", default=None)
    """The unique identifier for the account."""

    exchange_type: Optional[
        Literal["BINANCE", "BINANCE_MARGIN", "B2C2", "WINTERMUTE", "BLOCKFILLS", "STONEX"]
    ] = FieldInfo(alias="exchangeType", default=None)
    """Exchange type"""

    interval: Optional[Literal["1s", "1m", "5m", "15m", "30m", "1h", "2h", "1d", "1w"]] = None

    symbol: Optional[str] = None


Payload = Union[
    PayloadQuoteRequest,
    PayloadPlaceOrderRequest,
    PayloadCancelOrderRequest,
    Quote,
    Order,
    ExecutionReport,
    PayloadExchangeAccountPortfolio,
    Orderbook,
    PayloadKline,
]


class Event(BaseModel):
    event_id: str = FieldInfo(alias="eventId")
    """A unique identifier for the event."""

    event_type: str = FieldInfo(alias="eventType")
    """The type of the event (e.g., order, executionReport, portfolio, orderBook)."""

    timestamp: int
    """Unix timestamp in milliseconds when the event was generated."""

    payload: Optional[Payload] = None
    """The actual data of the event, which varies based on the event type."""

    source: Optional[str] = None
    """The source system or module that generated the event."""
