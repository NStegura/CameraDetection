from fastapi import APIRouter, Body, Form
from starlette.responses import HTMLResponse

auth = APIRouter(prefix='/auth', tags=['auth'])


@auth.post('/')
async def login(name: str = Form(...)):
    return "{dfgdfgdf}"


