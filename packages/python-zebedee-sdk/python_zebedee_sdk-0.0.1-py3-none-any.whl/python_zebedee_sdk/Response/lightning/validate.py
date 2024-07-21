from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Name(BaseModel):
    mandatory: bool


class Identifier(BaseModel):
    mandatory: bool


class PayerData(BaseModel):
    name: Name
    identifier: Identifier


class Metadata(BaseModel):
    min_sendable: int = Field(..., alias='minSendable')
    max_sendable: int = Field(..., alias='maxSendable')
    comment_allowed: int = Field(..., alias='commentAllowed')
    tag: str
    metadata: str
    callback: str
    payer_data: PayerData = Field(..., alias='payerData')
    disposable: bool


class Data(BaseModel):
    valid: bool
    metadata: Metadata


class ValidateResponse(BaseModel):
    success: Optional[bool] = None
    data: Optional[Data] = None
