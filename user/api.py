from fastapi import APIRouter, Body, Form
from starlette.requests import Request
from settings.settings import TEMPLATES
from . import schemas, services

user_router = APIRouter(prefix='/auth', tags=['auth'])


# @user_router.get('/')
# async def google_auth(request: Request):
#     return TEMPLATES.TemplateResponse("auth.html", {"request": request})
#
#
# @user_router.post('/google/auth', response_model=schemas.Token)
# async def google_auth(user: schemas.UserCreate):
#     user_id, token = await services.google_auth(user)
#     return schemas.Token(id=user_id, token=token)