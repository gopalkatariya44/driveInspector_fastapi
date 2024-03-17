import logging
from typing import Annotated

import beanie
import pymongo
from fastapi import APIRouter, HTTPException, status, Body, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import ValidationError

from core.config import settings
from core.security import create_access_token, create_refresh_token, get_current_user

from features.users.user_schemas import (CreateUserRequest, Token, TokenPayload,
                                         LoginUserRequest, DeleteUserRequest, CreateTokenBlackList)
from features.users.user_services import UserService

router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUserRequest):
    try:
        data = await UserService.create_user(user)
        print(f"User Created: {data}")
        return data
    except (pymongo.errors.DuplicateKeyError, beanie.exceptions.RevisionIdWasChanged):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username or email already exist."
        )


@router.post("/login_dict", response_model=Token)
async def login_for_access_token(response: Response, data: LoginUserRequest):
    # try:
    user = await UserService.authenticate(email=data.email, password=data.password)
    if user is None:
        print("hey")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect email or password"
        )
    # create access amd refresh token
    tokens = {
        'access_token': create_access_token(user.user_id),
        'refresh_token': create_refresh_token(user.user_id),
        'token_type': 'bearer'
    }
    # response.set_cookie(key="access_token", value=tokens['access_token'], httponly=True)
    # response.set_cookie(key="refresh_token", value=tokens['refresh_token'], httponly=True)

    print(f"access_token: {tokens['access_token']}")
    print(f"refresh_token: {tokens['refresh_token']}")

    return tokens
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Somthing went wrong"
    #     )


@router.post("/logout")
async def logout(token: CreateTokenBlackList, user: dict = Depends(get_current_user)):
    try:
        data = await UserService.add_token_to_black_list(token)
        print(f"User Logout: {data}")
        return {"message": "Logout successful"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something went wrong"
        )


@router.post('/refresh', summary="Refresh token", response_model=Token)
async def refresh_token(refresh_token: str = Body(...)):
    try:
        payload = jwt.decode(refresh_token, settings.REFRESH_SECRET_KEY, algorithms=settings.ALGORITHM)
        token_data = TokenPayload(**payload)
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = await UserService.get_user_by_id(token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not find user",
        )
    tokens = {
        'access_token': create_access_token(user.user_id),
        'refresh_token': create_refresh_token(user.user_id)
    }
    print(f"access_token: {tokens['access_token']}")
    print(f"refresh_token: {tokens['refresh_token']}")
    return tokens


@router.delete("/delete")
async def delete_user(data: DeleteUserRequest, user: dict = Depends(get_current_user)):
    try:
        await UserService.delete_user(data.user_id)
        print(f"User Deleted: {data}")
        return {"message": "User deleted successful"}
    except Exception as e:
        print(e)


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user = await UserService.authenticate(email=form_data.username, password=form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password"
            )
        tokens = {
            'access_token': create_access_token(user.user_id),
            'refresh_token': create_refresh_token(user.user_id),
            'token_type': 'bearer'
        }
        print(f"access_token: {tokens['access_token']}")
        print(f"refresh_token: {tokens['refresh_token']}")
        # create access amd refresh token
        return tokens
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Somthing went wrong"
        )
