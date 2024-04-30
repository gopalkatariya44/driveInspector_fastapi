import os
from uuid import UUID
from bson import ObjectId
from fastapi import APIRouter, Request, status, Form, UploadFile
from starlette.responses import FileResponse, HTMLResponse, RedirectResponse

from core.config import settings
from core.security import get_current_user
from features import templates
from features.camera_feed.camera_feed_services import CameraFeedServices
from features.detection_ocr.detection_ocr_services import DetectionOCRServices
from features.vehicle_details.vehicle_details_services import VehicleDetailsServices

router = APIRouter(
    tags=['Camera Feed']
)


@router.get('/', response_class=HTMLResponse)
async def camera_feed(request: Request, page: int = 1, limit: int = 100, target_timezone: str = 'Asia/Kolkata'):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/user/login', status_code=status.HTTP_302_FOUND)
    camera_feed_list = await CameraFeedServices.get_list(user.user_id, page, limit)
    return templates.TemplateResponse(
        'home.html', {"request": request,
                      'camera_feed_list': camera_feed_list,
                      'user_id': user.user_id,
                      'ai_service_url': settings.AI_SERVICE_URL,
                      "target_timezone": target_timezone
                      })


@router.get('/add', response_class=HTMLResponse)
async def auth_page(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/user/login', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse('camera_feed/add_camera_feed.html',
                                      {'request': request})


@router.post('/add', response_class=HTMLResponse)
async def auth_page(request: Request, video_file: UploadFile = Form(...),
                    rtsp_url: str = Form(...),
                    media_type: int = Form(...)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/user/login', status_code=status.HTTP_302_FOUND)
    video_path = rtsp_url
    if media_type == 1:
        video_byte = await video_file.read()
        folder_path = f"static/users/{user.user_id}/input"
        video_path = f"static/users/{user.user_id}/input/{video_file.filename}"

        os.makedirs(folder_path, exist_ok=True)
        with open(video_path, 'wb') as f:
            f.write(video_byte)
    await CameraFeedServices.add(user.user_id, video_path)
    return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)


@router.get('/edit/{id}', response_class=HTMLResponse)
async def auth_page(id: str, request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/user/login', status_code=status.HTTP_302_FOUND)
    camera_feed_id = ObjectId(id)
    camera_feed_details = dict(await CameraFeedServices.get_one(camera_feed_id))

    return templates.TemplateResponse('camera_feed/update_camera_feed.html',
                                      {'request': request, 'camera_feed_details': camera_feed_details})


@router.post('/update/{id}', response_class=HTMLResponse)
async def auth_page(id: str, request: Request, video_file: UploadFile = Form(...)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/user/login', status_code=status.HTTP_302_FOUND)

    camera_feed_id = ObjectId(id)
    detection_details = dict(await CameraFeedServices.get_one(camera_feed_id))

    video_byte = await video_file.read()
    folder_path = f"static/users/{user.user_id}/input"
    video_path = f"static/users/{user.user_id}/input/{video_file.filename}"
    os.makedirs(folder_path, exist_ok=True)

    with open(video_path, 'wb') as f:
        f.write(video_byte)
    detection_details['media_url'] = video_path
    await CameraFeedServices.update(camera_feed_id, detection_details)
    return RedirectResponse(url=f'/', status_code=status.HTTP_302_FOUND)


@router.get('/delete/{id}', response_class=HTMLResponse)
async def delete(id: str, request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/user/login', status_code=status.HTTP_302_FOUND)
    camera_feed_id = ObjectId(id)
    await CameraFeedServices.delete(camera_feed_id)
    return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
