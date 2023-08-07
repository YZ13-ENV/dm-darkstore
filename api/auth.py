from typing import Union
from services.authService import AuthService
from fastapi import APIRouter, Response
from fastapi.responses import Response

router = APIRouter(
    prefix='/auth',
    tags=['Авторизация']
)


@router.post('/authComplete')
async def authComplete(email: str):
    service = AuthService()
    uid: Union[str, None] = await service.returnAuthoredUser(email=email)
    if not uid:
        res = Response(status_code=200)
        return res
    else:
        res = Response(status_code=200)
        res['accessToken'] = uid
        return res
