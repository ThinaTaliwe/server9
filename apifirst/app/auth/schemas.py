"""Pydantic schemas for authentication.

Defines request and response models for users, clients and tokens.
"""

from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = Field(default="bearer")
    expires_in: int


class UserBase(BaseModel):
    username: str
    email: EmailStr | None = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime

    class Config:
        orm_mode = True


class ClientRead(BaseModel):
    id: int
    client_id: str
    label: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True