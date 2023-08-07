from services.authService import AuthService
from fastapi import APIRouter, Response

router = APIRouter(
    prefix='/auth',
    tags=['Авторизация']
)


@router.post('/authComplete')
async def authComplete(email: str, res: Response):
    service = AuthService()
    res = await service.returnAuthoredUser(res=res, email=email)
    if not res:
        return False
    return True