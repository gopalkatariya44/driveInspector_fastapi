from bson import ObjectId
from fastapi import APIRouter, Request, status
from starlette.responses import FileResponse, HTMLResponse, RedirectResponse

from core.config import settings
from core.security import get_current_user
from features import templates
from features.vehicle_details.vehicle_details_services import VehicleDetailsServices

router = APIRouter(
    tags=['Vehicle Details']
)


@router.get('/list')
async def vehicle_list(page: int = 1, limit: int = 100):
    vehicle_details_list = await VehicleDetailsServices.get_list(page, limit)
    return vehicle_details_list


@router.get('/', response_class=HTMLResponse)
async def vehicle_list(request: Request, page: int = 1, limit: int = 100):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/user/login', status_code=status.HTTP_302_FOUND)
    vehicle_details_list = await VehicleDetailsServices.get_list(user.user_id, page, limit)
    return templates.TemplateResponse(
        'home.html',
        {
            "request": request,
            'vehicle_details_list': vehicle_details_list,
            'user_id': user.user_id,
            'ai_service_url': settings.AI_SERVICE_URL
        }
    )


@router.get("/get_image", response_class=HTMLResponse)
async def getfile(request: Request, file_path: str):
    global img
    img = file_path
    return templates.TemplateResponse(
        'vehicle_details/image.html',
        {
            'request': request,
            'image_path': file_path
        }
    )


@router.get('/details/{id}', response_class=HTMLResponse)
async def vehicle_list(id: str, request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/user/login', status_code=status.HTTP_302_FOUND)
    global img
    user_id = ObjectId(id)
    vehicle_details = dict(await VehicleDetailsServices.get_one(user_id))
    vehicle_details['img_url'] = vehicle_details['img_url'].replace("../driveinspector_fastapi", "")
    return templates.TemplateResponse(
        'vehicle_details/vehicle_details.html',
        {
            'request': request,
            'vehicle_details': vehicle_details
        }
    )
