from uuid import UUID
from bson import ObjectId
from fastapi import APIRouter, Request, status, Form
from starlette.responses import FileResponse, HTMLResponse, RedirectResponse

from core.config import settings
from core.security import get_current_user
from features import templates
from features.detection_ocr.detection_ocr_services import DetectionOCRServices

router = APIRouter(
    tags=['Detection OCR']
)


@router.get('/list')
async def detection_list(page: int = 1, limit: int = 100):
    detection_ocr_list = await DetectionOCRServices.get_list(page, limit)
    return detection_ocr_list


@router.get('/', response_class=HTMLResponse)
async def detection_list(request: Request, page: int = 1, limit: int = 100, target_timezone: str = 'Asia/Kolkata'):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/user/login', status_code=status.HTTP_302_FOUND)
    print("user>>>>", user.user_id)
    detection_ocr_list = await DetectionOCRServices.get_list(user.user_id, page, limit)
    print(type(detection_ocr_list))
    print("detection_ocr_list>>>>>>>>>>>>>>>>>>>>>", detection_ocr_list)
    return templates.TemplateResponse(
        'home.html', {"request": request,
                      'detection_ocr_list': detection_ocr_list,
                      'user_id': user.user_id,
                      'ai_service_url': settings.AI_SERVICE_URL,
                      "target_timezone": target_timezone
                      })


@router.get('/details/{id}', response_class=HTMLResponse)
async def detection_list(id: str, request: Request, target_timezone: str = 'Asia/Kolkata'):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/user/login', status_code=status.HTTP_302_FOUND)
    user_id = ObjectId(id)
    detection_details = dict(await DetectionOCRServices.get_one(user_id))
    detection_details['img_url'] = detection_details['img_url'].replace("../driveinspector_fastapi", "")
    print(detection_details)
    return templates.TemplateResponse(
        'detection_details/detection_details.html',
        {
            'request': request,
            'detection_details': detection_details,
            "target_timezone": target_timezone
        }
    )


@router.get('/edit/{id}', response_class=HTMLResponse)
async def auth_page(id: str, request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/user/login', status_code=status.HTTP_302_FOUND)
    user_id = ObjectId(id)
    detection_details = dict(await DetectionOCRServices.get_one(user_id))
    detection_details['img_url'] = detection_details['img_url'].replace("../driveinspector_fastapi", "")
    return templates.TemplateResponse('detection_details/update_detection_details.html',
                                      {'request': request, 'detection_details': detection_details})


@router.post('/update/{id}', response_class=HTMLResponse)
async def auth_page(id: str, request: Request, reg_no: str = Form(...)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/user/login', status_code=status.HTTP_302_FOUND)
    id = ObjectId(id)
    detection_details = dict(await DetectionOCRServices.get_one(id))
    detection_details['reg_no'] = reg_no
    await DetectionOCRServices.update(id, detection_details)
    return RedirectResponse(url=f'/details/{id}', status_code=status.HTTP_302_FOUND)


@router.get('/delete/{id}', response_class=HTMLResponse)
async def delete(id: str, request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/user/login', status_code=status.HTTP_302_FOUND)
    detection_details_id = ObjectId(id)
    await DetectionOCRServices.delete(detection_details_id)
    return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
