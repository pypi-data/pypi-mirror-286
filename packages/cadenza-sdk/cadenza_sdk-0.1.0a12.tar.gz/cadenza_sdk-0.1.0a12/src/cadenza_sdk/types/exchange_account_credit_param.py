# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ExchangeAccountCreditParam"]


class ExchangeAccountCreditParam(TypedDict, total=False):
    account_type: Annotated[Literal["SPOT", "MARGIN"], PropertyInfo(alias="accountType")]
    """Type of account (SPOT, MARGIN)"""

    credit: float
    """The amount of credit available to the account from the broker or exchange"""

    currency: str

    exchange_account_id: Annotated[str, PropertyInfo(alias="exchangeAccountId")]

    exchange_type: Annotated[
        Literal["BINANCE", "BINANCE_MARGIN", "B2C2", "WINTERMUTE", "BLOCKFILLS", "STONEX"],
        PropertyInfo(alias="exchangeType"),
    ]
    """Exchange type"""

    leverage: int
    """The maximum leverage the account have"""

    margin: float
    """
    The amount of collateral that the investor has deposited in the account to cover
    potential losses
    """

    margin_level: Annotated[float, PropertyInfo(alias="marginLevel")]
    """The rate between equity and margin requirement"""

    margin_loan: Annotated[float, PropertyInfo(alias="marginLoan")]
    """The amount of money borrowed from the broker to purchase securities"""

    margin_requirement: Annotated[float, PropertyInfo(alias="marginRequirement")]
    """The amount of collateral required to maintain the current positions"""

    margin_usage: Annotated[float, PropertyInfo(alias="marginUsage")]
    """The rate to which the available margin is being utilized"""

    max_risk_exposure: Annotated[float, PropertyInfo(alias="maxRiskExposure")]
    """
    The maximum value of risk exposure that the account can handle, set to manage
    risk and avoid excessive exposure to market volatility
    """

    risk_exposure: Annotated[float, PropertyInfo(alias="riskExposure")]
    """
    The total value of positions held in the account, indicating the level of market
    exposure
    """

    risk_exposure_rate: Annotated[float, PropertyInfo(alias="riskExposureRate")]
    """The rate between risk exposure and max risk exposure"""
