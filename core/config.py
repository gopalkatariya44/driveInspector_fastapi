from typing import List
from pydantic import AnyHttpUrl
from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SatView3D"
    JWT_SECRET_KEY: str = config('JWT_SECRET_KEY', cast=str)
    REFRESH_SECRET_KEY: str = config('REFRESH_SECRET_KEY', cast=str)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config('ACCESS_TOKEN_EXPIRE_MINUTES', cast=int)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = config('REFRESH_TOKEN_EXPIRE_MINUTES', cast=int)
    # SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL', cast=str)

    # Database
    MONGO_CONNECTION_STRING: str = config("MONGO_CONNECTION_STRING", cast=str)
    DB_NAME: str = config("DB_NAME", cast=str)
    BACKEND_CORS_ORIGINS: list = config("BACKEND_CORS_ORIGINS", cast=str).split(',')


    class Config:
        case_sensitive = True


settings = Settings()
