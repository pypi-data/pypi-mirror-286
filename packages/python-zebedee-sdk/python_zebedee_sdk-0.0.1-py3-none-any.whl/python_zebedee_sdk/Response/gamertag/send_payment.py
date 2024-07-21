from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Data(BaseModel):
    id: str
    status: str
    transaction_id: str = Field(..., alias='transactionId')
    receiver_id: str = Field(..., alias='receiverId')
    amount: str
    comment: str
    settled_at: str = Field(..., alias='settledAt')


class SendPaymentResponse(BaseModel):
    success: Optional[bool] = None
    data: Optional[Data] = None
    message: Optional[str] = None
