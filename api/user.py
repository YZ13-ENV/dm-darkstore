

from fastapi import APIRouter

from services.userService import UserService
router = APIRouter(
    prefix='/users',
    tags=['Пользователи']
)

@router.get('/shortData')
async def getShortData(userId: str):
    service = UserService(userId)
    data = await service.getShortData()
    return data