from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Data(BaseModel):
    gamertag: str


class GetGamerTagResponse(BaseModel):
    success: Optional[bool] = None
    data: Optional[Data] = None
    message: Optional[str] = None
