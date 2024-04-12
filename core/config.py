from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str  # = config('PROJECT_NAME', cast=str)
    JWT_SECRET_KEY: str  # = config('JWT_SECRET_KEY', cast=str)
    REFRESH_SECRET_KEY: str  # = config('REFRESH_SECRET_KEY', cast=str)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int  # = config('ACCESS_TOKEN_EXPIRE_MINUTES', cast=int)
    REFRESH_TOKEN_EXPIRE_MINUTES: int  # = config('REFRESH_TOKEN_EXPIRE_MINUTES', cast=int)
    # SQLALCHEMY_DATABASE_URL # = config('SQLALCHEMY_DATABASE_URL', cast=str)

    # Database
    MONGO_CONNECTION_STRING: str  # = config("MONGO_CONNECTION_STRING", cast=str)
    DB_NAME: str  # = config("DB_NAME", cast=str)
    BACKEND_CORS_ORIGINS: str  # = config("BACKEND_CORS_ORIGINS", cast=str).split(',')

    AI_SERVICE_URL: str  # = config

    # class Config:
    #     case_sensitive = True

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
