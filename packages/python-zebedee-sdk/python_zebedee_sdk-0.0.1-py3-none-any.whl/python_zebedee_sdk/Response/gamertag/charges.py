from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class Data(BaseModel):
    unit: str
    status: str
    amount: str
    created_at: str = Field(..., alias='createdAt')
    internal_id: str = Field(..., alias='internalId')
    callback_url: str = Field(..., alias='callbackUrl')
    description: str
    invoice_request: str = Field(..., alias='invoiceRequest')
    invoice_expires_at: str = Field(..., alias='invoiceExpiresAt')
    invoice_description_hash: Any = Field(..., alias='invoiceDescriptionHash')


class ChargesResponse(BaseModel):
    success: Optional[bool] = None
    data: Optional[Data] = None
