from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Data(BaseModel):
    amount: str
    ln_request: str = Field(..., alias='lnRequest')
    ln_expires_at: str = Field(..., alias='lnExpiresAt')
    network: str
    description: str
    description_hash: str = Field(..., alias='descriptionHash')
    payment_hash: str = Field(..., alias='paymentHash')
    payment_secret: str = Field(..., alias='paymentSecret')
    payee: str
    signature: str


class DecodeChargeResponse(BaseModel):
    success: Optional[bool] = None
    data: Optional[Data] = None
