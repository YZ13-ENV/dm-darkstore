from typing import Optional
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

@router.get('/token')
async def getTokenToAuth(userId: str):
    service = UserService(userId=userId)
    token = await service.generateCustomToken()
    return token

@router.patch('/updateUser')
async def updateUser(userId: str, displayName: Optional[str]=None, photoUrl: Optional[str]=None):
    service = UserService(userId=userId)
    isComplete = service.updateUser(displayName, photoUrl)
    return isComplete

@router.get('/shortByEmail')
async def getShortByEmail(email: str):
    service = UserService('')
    shortData = await service.getShortDataByEmail(email)
    return shortData