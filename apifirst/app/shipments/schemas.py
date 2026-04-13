"""Pydantic schemas for shipments and related entities."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, constr


class TagBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=64)


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class FollowerCreate(BaseModel):
    email: constr(strip_whitespace=True, min_length=3, max_length=255)


class FollowerRead(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


class ShipmentBase(BaseModel):
    reference: constr(strip_whitespace=True, min_length=1, max_length=64)
    container_number: constr(strip_whitespace=True, min_length=1, max_length=64)
    booking_number: Optional[constr(strip_whitespace=True, max_length=64)] = None
    carrier_code: Optional[str] = Field(None, description="Code of the carrier")


class ShipmentCreate(ShipmentBase):
    tags: Optional[List[str]] = Field(default_factory=list)
    followers: Optional[List[str]] = Field(default_factory=list)


class ShipmentUpdate(BaseModel):
    reference: Optional[str] = None
    # Additional updatable fields can be added here


class ShipmentRead(BaseModel):
    id: int
    reference: str
    container_number: str
    booking_number: Optional[str]
    carrier_code: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    tags: List[TagRead] = []
    followers: List[FollowerRead] = []

    class Config:
        orm_mode = True