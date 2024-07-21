from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class Invoice(BaseModel):
    request: str
    uri: str


class Data(BaseModel):
    unit: str
    amount: str
    confirmed_at: Any = Field(..., alias='confirmedAt')
    status: str
    description: str
    created_at: str = Field(..., alias='createdAt')
    expires_at: str = Field(..., alias='expiresAt')
    id: str
    internal_id: str = Field(..., alias='internalId')
    callback_url: str = Field(..., alias='callbackUrl')
    invoice: Invoice


class CreateChargeResponse(BaseModel):
    success: Optional[bool] = None
    message: Optional[str] = None
    data: Optional[Data] = None
