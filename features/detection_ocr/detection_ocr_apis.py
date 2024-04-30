from uuid import UUID
from bson import ObjectId
from fastapi import APIRouter, Request, status, Form
from starlette.responses import FileResponse, HTMLResponse, RedirectResponse

from core.config import settings
from core.security import get_current_user
from features import templates
from features.detection_ocr.detection_ocr_services import DetectionOCRServices
from features.vehicle_details.vehicle_details_services import VehicleDetailsServices

router = APIRouter(
    prefix='/detection-ocr',
    tags=['Detection OCR']
)


@router.get('/list')
async def detection_list_dict(camera_feed_id: UUID, page: int = 1, limit: int = 100):
    detection_ocr_list = await DetectionOCRServices.get_list(camera_feed_id, page, limit)
    return detection_ocr_list


@router.get('/{camera_feed_id}', response_class=HTMLResponse)
async def detection_list(camera_feed_id: UUID, request: Request, page: int = 1, limit: int = 100,
                         target_timezone: str = 'Asia/Kolkata'):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/user/login', status_code=status.HTTP_302_FOUND)
    detection_ocr_list = await DetectionOCRServices.get_list(camera_feed_id, page, limit)
    return templates.TemplateResponse(
        'detection_details/detection_list.html',
        {"request": request,
         'detection_ocr_list': detection_ocr_list,
         'user_id': user.user_id,
         'camera_feed_id': camera_feed_id,
         'ai_service_url': settings.AI_SERVICE_URL,
         "target_timezone": target_timezone
         })


@router.get('/details/{id}', response_class=HTMLResponse)
async def detection_details(id: UUID, request: Request, target_timezone: str = 'Asia/Kolkata'):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/user/login', status_code=status.HTTP_302_FOUND)
    # id = ObjectId(id)
    detection_details = dict(await DetectionOCRServices.get_one(id))
    detection_details['img_url'] = detection_details['img_url'].replace("../driveinspector_fastapi", "")
    vehicle_details = dict(await VehicleDetailsServices.get_by_regno(detection_details['reg_no']))
    return templates.TemplateResponse(
        'detection_details/detection_details.html',
        {
            'request': request,
            'detection_details': detection_details,
            'vehicle_details': vehicle_details,
            "target_timezone": target_timezone
        }
    )


@router.get('/edit/{detection_ocr_id}', response_class=HTMLResponse)
async def edit_details(detection_ocr_id: UUID, request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/user/login', status_code=status.HTTP_302_FOUND)
    # user_id = ObjectId(id)
    detection_details = dict(await DetectionOCRServices.get_one(detection_ocr_id))
    detection_details['img_url'] = detection_details['img_url'].replace("../driveinspector_fastapi", "")
    return templates.TemplateResponse('detection_details/update_detection_details.html',
                                      {'request': request, 'detection_details': detection_details})


@router.post('/update/{id}', response_class=HTMLResponse)
async def update_details(id: UUID, request: Request, reg_no: str = Form(...)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/user/login', status_code=status.HTTP_302_FOUND)
    detection_details = dict(await DetectionOCRServices.get_one(id))
    detection_details['reg_no'] = reg_no
    await DetectionOCRServices.update(id, detection_details)
    return RedirectResponse(url=f'/detection-ocr/details/{id}', status_code=status.HTTP_302_FOUND)


@router.get('/email/{reg_no}/{camera_feed_id}', response_class=HTMLResponse)
async def email(reg_no: str, camera_feed_id: UUID, request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/user/login', status_code=status.HTTP_302_FOUND)
    # detection_details = dict(await DetectionOCRServices.get_one(user_id))
    # vehicle_details = dict(await VehicleDetailsServices.get_by_regno(reg_no))

    await VehicleDetailsServices.generate_challan_pdf(reg_no)
    return RedirectResponse(url=f'/detection-ocr/{camera_feed_id}', status_code=status.HTTP_302_FOUND)


@router.get('/delete/{detection_ocr_id}/{camera_feed_id}', response_class=HTMLResponse)
async def delete(detection_ocr_id: UUID, camera_feed_id: UUID, request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/user/login', status_code=status.HTTP_302_FOUND)
    # detection_details_id = ObjectId(id)
    await DetectionOCRServices.delete(detection_ocr_id)
    return RedirectResponse(url=f'/detection-ocr/{camera_feed_id}', status_code=status.HTTP_302_FOUND)
