from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings
from features.users.user_models import UserModel, TokenBlackListModel
from features.vehicle_details.vehicle_details_model import VehicleDetailsModel


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # code to execute when app is loading
    mongo_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    await init_beanie(
        database=mongo_client[settings.DB_NAME],
        document_models=[
            UserModel,
            TokenBlackListModel,
            VehicleDetailsModel
        ]
    )
    print("[START]: Initialize application services")
    yield
    # code to execute when app is shutting down


# @app.on_event('startup')
# async def app_init():
#     """
#     initialize crucial app services
#     """
#     mongo_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
#
#     # users = mongo_client["users"]
#     # await users.create_index([("email", ASCENDING)], unique=True)
#
#     await init_beanie(
#         database=mongo_client[settings.DB_NAME],
#         document_models=[
#             UserModel,
#             TokenBlackListModel,
#         ]
#     )
#     print("[START]: Initialize application services")