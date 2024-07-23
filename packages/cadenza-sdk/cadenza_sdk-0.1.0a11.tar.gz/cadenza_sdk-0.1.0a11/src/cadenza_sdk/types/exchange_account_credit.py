# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ExchangeAccountCredit"]


class ExchangeAccountCredit(BaseModel):
    account_type: Optional[Literal["SPOT", "MARGIN"]] = FieldInfo(alias="accountType", default=None)
    """Type of account (SPOT, MARGIN)"""

    credit: Optional[float] = None
    """The amount of credit available to the account from the broker or exchange"""

    currency: Optional[str] = None

    exchange_account_id: Optional[str] = FieldInfo(alias="exchangeAccountId", default=None)

    exchange_type: Optional[
        Literal["BINANCE", "BINANCE_MARGIN", "B2C2", "WINTERMUTE", "BLOCKFILLS", "STONEX"]
    ] = FieldInfo(alias="exchangeType", default=None)
    """Exchange type"""

    leverage: Optional[int] = None
    """The maximum leverage the account have"""

    margin: Optional[float] = None
    """
    The amount of collateral that the investor has deposited in the account to cover
    potential losses
    """

    margin_level: Optional[float] = FieldInfo(alias="marginLevel", default=None)
    """The rate between equity and margin requirement"""

    margin_loan: Optional[float] = FieldInfo(alias="marginLoan", default=None)
    """The amount of money borrowed from the broker to purchase securities"""

    margin_requirement: Optional[float] = FieldInfo(alias="marginRequirement", default=None)
    """The amount of collateral required to maintain the current positions"""

    margin_usage: Optional[float] = FieldInfo(alias="marginUsage", default=None)
    """The rate to which the available margin is being utilized"""

    max_risk_exposure: Optional[float] = FieldInfo(alias="maxRiskExposure", default=None)
    """
    The maximum value of risk exposure that the account can handle, set to manage
    risk and avoid excessive exposure to market volatility
    """

    risk_exposure: Optional[float] = FieldInfo(alias="riskExposure", default=None)
    """
    The total value of positions held in the account, indicating the level of market
    exposure
    """

    risk_exposure_rate: Optional[float] = FieldInfo(alias="riskExposureRate", default=None)
    """The rate between risk exposure and max risk exposure"""
