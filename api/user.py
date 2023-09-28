import os
import jwt
import datetime
from typing import Optional, Union
from fastapi import APIRouter, Header
from fastapi_cache.decorator import cache
from database.user import getRecommendationTags, setPlusSubscription
from services.userService import UserService
from firebase import db

router = APIRouter(
    prefix='/users',
    tags=['Пользователи']
)

@router.get('/shortData')
@cache(expire=120)
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
@cache(expire=120)
async def getShortByEmail(email: str):
    service = UserService('')
    shortData = await service.getShortDataByEmail(email)
    return shortData

@router.post('/startFollow')
async def startFollow(userId: str, followId: str):
    service = UserService(userId=userId)
    isEnded = await service.startFollow(followId=followId)
    return isEnded    

@router.get('/isInFollowList')
async def isInFollowList(userId: str, followId: str):
    service = UserService(userId=userId)
    isInList = await service.isInFollowList(followId=followId)
    return isInList

@router.post('/stopFollow')
async def stopFollow(userId: str, followId: str):
    service = UserService(userId=userId)
    isEnded = await service.stopFollow(followId=followId)
    return isEnded

@router.get('/accessToSub')
async def getAccessToSub(token: Union[str, None] = Header(default=None)):
    try:
        if (token):
            tokenData = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'], options={"verify_iat":False})
            iat = tokenData.get('iat')
            verifyToken = tokenData.get('verifyToken')
            now = datetime.datetime.now().timestamp()
            if (now > iat or not iat or verifyToken != os.getenv('TOKEN')):
                return None
            else: 
                tokenPayload = {
                    'iat': (datetime.datetime.now() + datetime.timedelta(minutes=5)).timestamp(),
                    'verifyToken': os.getenv('TOKEN')
                }
                return jwt.encode(tokenPayload, os.getenv('JWT_SECRET'), algorithm='HS256')
        else:
            return None
    except:
        return None

@router.get('/recommendations')
async def getUserRecommendationTags(userId: str):
    tags = await getRecommendationTags(userId=userId)
    return tags

@router.post('/setSubStatus')
async def setSubStatus(userId: str, status: bool=False, token: Union[str, None] = Header(default=None)):
    try:
        if (token):
            tokenData = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'], options={"verify_iat":False})
            iat = tokenData.get('iat')
            verifyToken = tokenData.get('verifyToken')
            now = datetime.datetime.now().timestamp()
            if (now > iat or not iat or verifyToken != os.getenv('TOKEN')):
                return None
            else: 
                res = await setPlusSubscription(userId=userId, subscriptionStatus=status)
                return res
        else:
            return None
    except:
        return None