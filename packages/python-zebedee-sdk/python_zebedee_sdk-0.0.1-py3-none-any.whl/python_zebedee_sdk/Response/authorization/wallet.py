from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class RemainingAmountLimits(BaseModel):
    daily: str
    max_credit: str = Field(..., alias='maxCredit')
    monthly: str
    weekly: str


class Data(BaseModel):
    balance: str
    remaining_amount_limits: RemainingAmountLimits = Field(
        ..., alias='remainingAmountLimits'
    )


class GetWalletResponse(BaseModel):
    message: Optional[str] = None
    success: Optional[bool] = None
    data: Optional[Data] = None
