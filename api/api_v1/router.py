from fastapi import APIRouter

from features.users import user_apis

api_v1_router = APIRouter(
    prefix='/v1'
)

# Auth APIs
api_v1_router.include_router(user_apis.router)
