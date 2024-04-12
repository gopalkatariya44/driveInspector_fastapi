from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from passlib.context import CryptContext
from core import security
from features.users.user_models import UserModel, TokenBlackListModel
from features.users.user_schemas import CreateUserRequest, CreateTokenBlackList

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    @staticmethod
    async def create_user(user: CreateUserRequest):
        user_in = UserModel(
            email=user.email,
            hashed_password=pwd_context.hash(user.password)
        )
        await user_in.save()
        return user_in

    @staticmethod
    async def add_token_to_black_list(token: CreateTokenBlackList):
        token_in = TokenBlackListModel(
            token=token.token,
            user_id=token.user_id
        )
        await token_in.insert()
        return token_in

    @staticmethod
    async def authenticate(email: str, password: str):
        user = await UserService.get_user_by_email(email=email)
        if not user:
            return False
        if not security.verify_password(password=password, hashed_password=user.hashed_password):
            return False
        return user

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[UserModel]:
        user = await UserModel.find_one(UserModel.email == email)
        return user

    @staticmethod
    async def get_user_by_id(user_id: UUID) -> Optional[UserModel]:
        user = await UserModel.find_one(UserModel.user_id == user_id)
        return user

    @staticmethod
    async def delete_user(user_id: UUID) -> Optional[UserModel]:
        user = await UserModel.delete(UserModel.user_id == user_id)
        return user
