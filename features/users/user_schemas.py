from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class CreateUserRequest(BaseModel):
    email: EmailStr = Field(..., description='user email')
    password: str = Field(..., min_length=6, max_length=24, description="user password")
    # created_at: datetime
    # updated_at: datetime


class UserResponse(BaseModel):
    user_id: UUID
    email: EmailStr
    created_at: datetime
    updated_at: datetime


class LoginUserRequest(BaseModel):
    email: EmailStr = Field(..., description='user email')
    password: str


class DeleteUserRequest(BaseModel):
    user_id: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: UUID = None
    exp: int = None


class CreateTokenBlackList(BaseModel):
    token: str
