from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Data(BaseModel):
    id: str


class GetIdResponse(BaseModel):
    success: Optional[bool] = None
    data: Optional[Data] = None
