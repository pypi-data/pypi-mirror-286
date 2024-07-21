from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Data(BaseModel):
    amount: str
    code: str
    created_at: str = Field(..., alias='createdAt')
    create_transaction_id: str = Field(..., alias='createTransactionId')
    description: str
    fee: str
    id: str
    unit: str
    wallet_id: str = Field(..., alias='walletId')


class CreateVoucherResponse(BaseModel):
    success: Optional[bool] = None
    data: Optional[Data] = None
    message: Optional[str] = None
