from fastapi import Depends, HTTPException, APIRouter, Request, Response

from starlette import status
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse

from core.security import get_current_user, create_access_token, create_refresh_token
from features import templates
from features.users.user_schemas import CreateUserRequest, CreateTokenBlackList
from features.users.user_services import UserService

router = APIRouter(
    prefix='/user',
    tags=['Auth'],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'user': 'Not authorized'
        }
    }
)


@router.get('/login', response_class=HTMLResponse)
async def auth_page(request: Request):
    user = await get_current_user(request)
    if user is not None:
        return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse('user/login.html', {'request': request})


@router.post('/login', response_class=HTMLResponse)
async def login(request: Request, response: Response):
    try:
        form = await request.form()
        user = await UserService.authenticate(email=form.get('email'), password=form.get('password'))

        if not user:
            msg = 'Incorrect Username or Password'
            return templates.TemplateResponse('user/login.html', {'request': request, 'msg': msg})

        redirect_response = RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
        redirect_response.set_cookie(key="access_token", value=create_access_token(user.user_id))
        redirect_response.set_cookie(key="refresh_token", value=create_refresh_token(user.user_id))

        return redirect_response
    except HTTPException:
        msg = 'Unknown Error'
        return templates.TemplateResponse('user/login.html', {'request': request, 'msg': msg})


@router.get('/register', response_class=HTMLResponse)
async def register_page(request: Request):
    user = await get_current_user(request)
    if user is not None:
        return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse('user/register.html', {'request': request})


@router.post('/register')
async def create_new_user(request: Request):
    form = await request.form()
    user = CreateUserRequest(
        email=form.get('email'),
        password=form.get('password')
    )
    try:
        await UserService.create_user(user)
        msg = 'User successfully created'
        response = templates.TemplateResponse('user/login.html', {'request': request, 'msg': msg})
        return response
    except Exception as e:
        msg = 'This username or email already exist.'
        if user is not None:
            return templates.TemplateResponse('user/register.html', {'request': request, 'msg': msg})


@router.get('/logout', response_class=HTMLResponse)
async def logout(request: Request):
    msg = 'Logout Successful'

    token = request.cookies.get('access_token')
    user = await get_current_user(request)
    data = CreateTokenBlackList(token=token, user_id=user.user_id)
    await UserService.add_token_to_black_list(data)

    response = templates.TemplateResponse('user/login.html', {'request': request, 'msg': msg})
    response.delete_cookie(key='access_token')
    response.delete_cookie(key='refresh_token')
    return response
