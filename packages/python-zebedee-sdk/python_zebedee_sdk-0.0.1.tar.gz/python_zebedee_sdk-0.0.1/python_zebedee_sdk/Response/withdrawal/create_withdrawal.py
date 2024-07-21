from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class Invoice(BaseModel):
    request: str
    fast_request: str = Field(..., alias='fastRequest')
    uri: str
    fast_uri: str = Field(..., alias='fastUri')


class Data(BaseModel):
    id: str
    unit: str
    amount: str
    created_at: str = Field(..., alias='createdAt')
    expires_at: str = Field(..., alias='expiresAt')
    internal_id: str = Field(..., alias='internalId')
    description: str
    callback_url: str = Field(..., alias='callbackUrl')
    status: str
    fee: Any
    invoice: Invoice


class CreateWithdrawalResponse(BaseModel):
    success: Optional[bool] = None
    data: Optional[Data] = None
    message: Optional[str] = None
