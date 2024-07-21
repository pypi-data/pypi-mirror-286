from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Data(BaseModel):
    unit: str
    balance: str


class GetWalletResponse(BaseModel):
    message: Optional[str] = None
    data: Optional[Data] = None
