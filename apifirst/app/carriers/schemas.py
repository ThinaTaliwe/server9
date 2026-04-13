"""Pydantic schemas for carriers."""

from datetime import datetime
from pydantic import BaseModel


class CarrierBase(BaseModel):
    code: str
    name: str


class CarrierRead(CarrierBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True