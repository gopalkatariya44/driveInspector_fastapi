from bson import ObjectId
from fastapi import APIRouter, Request
from starlette.responses import FileResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from features.vehicle_details.vehicle_details_services import VehicleDetailsServices

router = APIRouter(
    prefix='/vehicle_details',
    tags=['Vehicle Details']
)

templates = Jinja2Templates(directory='templates')
img = ''


@router.get('/list')
async def vehicle_list(page: int = 1, limit: int = 100):
    vehicle_details_list = await VehicleDetailsServices.get_list(page, limit)
    return vehicle_details_list


@router.get('/', response_class=HTMLResponse)
async def vehicle_list(request: Request, page: int = 1, limit: int = 100):
    vehicle_details_list = await VehicleDetailsServices.get_list(page, limit)
    return templates.TemplateResponse(
        'home.html',
        {
            'request': request,
            'vehicle_details_list': vehicle_details_list
        }
    )


@router.get("/get_image", response_class=HTMLResponse)
async def getfile(request: Request, file_path: str):
    global img
    img = file_path
    return templates.TemplateResponse(
        'image.html',
        {
            'request': request,
            'image_path': file_path
        }
    )


@router.get("/image", response_class=FileResponse)
async def get_image_file():
    global img
    return img.replace("../driveinspector_aicode/", "")


@router.get('/details/{id}', response_class=HTMLResponse)
async def vehicle_list(id: str, request: Request):
    global img
    user_id = ObjectId(id)
    vehicle_details = dict(await VehicleDetailsServices.get_one(user_id))
    print(vehicle_details)
    img = vehicle_details['img_url'].replace("../driveinspector_aicode/", "")
    return templates.TemplateResponse(
        'vehicle_details.html',
        {
            'request': request,
            'vehicle_details': vehicle_details
        }
    )
