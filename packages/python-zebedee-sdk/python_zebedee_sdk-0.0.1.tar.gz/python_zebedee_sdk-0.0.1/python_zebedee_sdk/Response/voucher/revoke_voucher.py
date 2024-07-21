from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class Data(BaseModel):
    amount: str
    code: str
    created_at: str = Field(..., alias='createdAt')
    description: str
    id: str
    redeemed_at: Any = Field(..., alias='redeemedAt')
    redeemed_by_id: Any = Field(..., alias='redeemedById')
    redeemed_transaction_id: Any = Field(..., alias='redeemedTransactionId')
    revoked_at: str = Field(..., alias='revokedAt')
    revoked_by_id: str = Field(..., alias='revokedById')
    revoked_transaction_id: str = Field(..., alias='revokedTransactionId')
    unit: str


class RevokeVoucherResponse(BaseModel):
    success: Optional[bool] = None
    data: Optional[Data] = None
    message: Optional[str] = None
