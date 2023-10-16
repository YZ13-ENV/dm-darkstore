from typing import Optional, Union
from fastapi import APIRouter
from fastapi_cache.decorator import cache
from database.user import getRecommendationTags
from firebase import db, auth
from firebase_admin import firestore
from helpers.nickname import getUidByNickName
# from helpers.nickname import getUidByNickName
from services.userService import UserService

router = APIRouter(
    prefix='/users',
    tags=['Пользователи']
)

# @router.get('/data/{nickname}')
# async def getDataByNickName(nickname: str):
#     uid = await getUidByNickName(nickname=nickname)
#     return uid
@router.get('/nickname/{nickname})
async def getNickname(nickname: str):
    userId: Union[str, None] = await getUidByNickName(nickname=nickname)
    return userId

@router.delete('/nickname/{nickname}')
async def removeNickName(nickname: str):
    nickRef: firestore.firestore.AsyncDocumentReference = db.collection('dm').document('users').collection('nicknames').document(nickname)
    await nickRef.delete()
    return None

@router.post('/nickname/{nickname}/{uid}')
async def setNickName(nickname: str, uid: str):
    kwargs = {
        'display_name': nickname
    }
    auth.update_user(uid=uid, **kwargs)
    nicknameDict = {
        'nickname': nickname,
        'uid': uid
    }
    nickRef: firestore.firestore.AsyncDocumentReference = db.collection('dm').document('users').collection('nicknames').document(nickname)
    await nickRef.set(document_data=nicknameDict)
    return None

@router.get('/short/nickname/{nickname}')
@cache(expire=120)
async def getShortData(nickname: str):
    userId: Union[str, None] = await getUidByNickName(nickname=nickname)
    if userId:
        service = UserService(userId)
        data = await service.getShortData()
        return data
    else:
        return None


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



@router.get('/recommendations')
async def getUserRecommendationTags(userId: str):
    tags = await getRecommendationTags(userId=userId)
    return tags

