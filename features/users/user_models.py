from enum import Enum
from typing import Optional
from uuid import uuid4, UUID
from datetime import datetime

from beanie import Document, Indexed, before_event, Insert, Replace
from pydantic import Field, EmailStr


class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class UserModel(Document):
    user_id: UUID = Field(default_factory=uuid4, unique=True)
    email: Indexed(EmailStr, unique=True)
    password: str
    role: UserRole = Field(default=UserRole.admin)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email}>"

    def __str__(self):
        return self.email

    def __hash__(self):
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, UserModel):
            return self.email == other.email
        return False

    @property
    def create(self) -> datetime:
        return self.id.generation_time

    async def by_email(self, email: str) -> "User":
        return await self.find_one(self.email == email)

    @before_event([Insert, Replace])
    def update_updated_at(self):
        self.updated_at = datetime.utcnow()

    class Settings:
        name = "users"


class TokenBlackListModel(Document):
    token: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "token_black_list"
