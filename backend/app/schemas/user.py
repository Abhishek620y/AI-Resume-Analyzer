"""Pydantic schemas for User — request/response validation for auth endpoints."""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, ConfigDict


class UserRoleSchema(str, Enum):
    ADMIN = "admin"
    RECRUITER = "recruiter"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRoleSchema = UserRoleSchema.RECRUITER


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    role: UserRoleSchema
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int | None = None
