from fastapi import APIRouter

from features.users import user_apis
from features.users import user_apis
from features.vehicle_details import vehicle_details_apis
from features.detection_ocr import detection_ocr_apis

api_v1_router = APIRouter()

# Auth APIs
api_v1_router.include_router(user_apis.router)
# api_v1_router.include_router(vehicle_details_apis.router)
api_v1_router.include_router(detection_ocr_apis.router)

from common import filters
