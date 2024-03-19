from datetime import datetime, timedelta
from typing import Any, Union

from fastapi import HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from core.config import settings
from features.users.user_models import UserModel, TokenBlackListModel
from features.users.user_schemas import TokenPayload

from features.users.user_services import UserService

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/login")
now = datetime.utcnow()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserModel:
    # token = request.cookies.get('access_token')
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=settings.ALGORITHM)
        token_data = TokenPayload(**payload)
        # check the token is inside a blacklist or not
        black_list_token = await TokenBlackListModel.find_one(TokenBlackListModel.token == token)
        if datetime.fromtimestamp(token_data.exp) < datetime.now() or black_list_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate user credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = await UserService.get_user_by_id(token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not find user",
        )
    return user


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = now + expires_delta
    else:
        expires_delta = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encod = {
        'exp': expires_delta,
        'sub': str(subject),
    }
    encoded_jwt = jwt.encode(to_encod, settings.JWT_SECRET_KEY, settings.ALGORITHM)

    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = now + expires_delta
    else:
        expires_delta = now + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encod = {
        'exp': expires_delta,
        'sub': str(subject),
    }
    encoded_jwt = jwt.encode(to_encod, settings.REFRESH_SECRET_KEY, settings.ALGORITHM)

    return encoded_jwt


def get_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)
