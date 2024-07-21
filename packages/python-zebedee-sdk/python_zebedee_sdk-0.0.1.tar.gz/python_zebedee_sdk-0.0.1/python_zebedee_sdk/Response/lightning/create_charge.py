from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Invoice(BaseModel):
    uri: str
    request: str


class Data(BaseModel):
    lnaddress: str
    amount: str
    invoice: Invoice


class CreateChargeResponse(BaseModel):
    success: Optional[bool] = None
    data: Optional[Data] = None
