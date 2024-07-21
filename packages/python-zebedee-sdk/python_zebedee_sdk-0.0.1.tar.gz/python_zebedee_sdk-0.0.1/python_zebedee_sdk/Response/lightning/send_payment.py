from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class Data(BaseModel):
    id: str
    fee: str
    unit: str
    amount: str
    invoice: str
    preimage: Any
    wallet_id: str = Field(..., alias='walletId')
    transaction_id: str = Field(..., alias='transactionId')
    callback_url: str = Field(..., alias='callbackUrl')
    internal_id: str = Field(..., alias='internalId')
    comment: str
    processed_at: str = Field(..., alias='processedAt')
    created_at: str = Field(..., alias='createdAt')
    status: str


class SendPaymentResponse(BaseModel):
    success: Optional[bool] = None
    data: Optional[Data] = None
    message: Optional[str] = None
