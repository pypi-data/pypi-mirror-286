from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Data(BaseModel):
    id: str
    receiver_id: str = Field(..., alias='receiverId')
    amount: str
    fee: str
    unit: str
    processed_at: str = Field(..., alias='processedAt')
    confirmed_at: str = Field(..., alias='confirmedAt')
    comment: str
    status: str


class TransactionResponse(BaseModel):
    message: Optional[str] = None
    success: Optional[bool] = None
    data: Optional[Data] = None
