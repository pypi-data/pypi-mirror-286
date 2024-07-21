from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Invoice(BaseModel):
    request: str
    fast_request: str = Field(..., alias='fastRequest')
    uri: str
    fast_uri: str = Field(..., alias='fastUri')


class Data(BaseModel):
    unit: str
    amount: str
    status: str
    created_at: str = Field(..., alias='createdAt')
    expires_at: str = Field(..., alias='expiresAt')
    description: str
    id: str
    internal_id: str = Field(..., alias='internalId')
    callback_url: str = Field(..., alias='callbackUrl')
    invoice: Invoice


class GetWithdrawalResponse(BaseModel):
    success: Optional[bool] = None
    message: Optional[str] = None
    data: Optional[Data] = None
