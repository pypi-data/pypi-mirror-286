from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class Invoice(BaseModel):
    request: str
    uri: str


class Data(BaseModel):
    id: str
    unit: str
    slots: int
    min_amount: str = Field(..., alias='minAmount')
    max_amount: str = Field(..., alias='maxAmount')
    created_at: str = Field(..., alias='createdAt')
    expires_at: Any = Field(..., alias='expiresAt')
    internal_id: str = Field(..., alias='internalId')
    description: str
    callback_url: str = Field(..., alias='callbackUrl')
    allowed_slots: int = Field(..., alias='allowedSlots')
    success_message: str = Field(..., alias='successMessage')
    status: str
    invoice: Invoice


class GetStaticChargeResponse(BaseModel):
    message: Optional[str] = None
    data: Optional[Data] = None
