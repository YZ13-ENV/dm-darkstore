from typing import Optional
from schemas.draft import  DraftToPublish
from schemas.shot import ShotData, ShotDataForUpload
from services.shotService import ShotService
from fastapi import APIRouter
from fastapi_cache.decorator import cache
from firebase import db
router = APIRouter(
    prefix='/shots',
    tags=['Работы']
)

@router.get('/onlyShots')
@cache(expire=60)
async def getOnlyShots(userId: str, asDoc: bool=True, limit: Optional[int]=None):
    service = ShotService(userId=userId)
    shots = await service.getShots(asDoc=asDoc, limit=limit)
    return shots

@router.get('/onlyDrafts')
@cache(expire=60)
async def getOnlyDrafts(userId: str, asDoc: bool=True):
    service = ShotService(userId=userId)
    drafts = await service.getDrafts(asDoc=asDoc)
    return drafts

@router.get('/allShots/{order}')
@cache(expire=60)
async def getPopularFromAllShots(order: Optional[str]='popular', userId: Optional[str]=None):
    service = ShotService(userId=userId)
    shots = await service.getAllUsersShots(order=order)
    return shots

@router.get('/v2/allShots')
@cache(expire=60)
async def getPopularFromAllShots(order: Optional[str]='popular', userId: Optional[str]=None):
    service = ShotService(userId=userId)
    shots = await service.getAllUpgradedUsersShots(order=order)
    return shots

@router.post('/updateShot')
async def updateShot(userId: str, shotId: str, shot: ShotData):
    service = ShotService(userId=userId)
    isDone = await service.updateShot(shotId=shotId, shot=shot)
    return isDone

@router.patch('/addOrRemoveLikes')
async def addOrRemoveLikes(shotAuthorId: str, shotId: str, uid: str):
    service = ShotService(userId=shotAuthorId)
    result = await service.addOrRemoveLikes(shotId=shotId, uid=uid)
    return result

@router.patch('/addView')
async def addViews(shotAuthorId: str, shotId: str, uid: str):
    service = ShotService(userId=shotAuthorId)
    result = await service.addView(shotId=shotId, uid=uid)
    return result

@router.post('/updateDraft')
async def updateDraft(userId: str, draftId: str, draft: ShotDataForUpload):
    service = ShotService(userId=userId)
    isDone = await service.updateDraft(draftId, draft=draft)
    return isDone

@router.post('/publishDraft')
async def publishDraft(userId: str, draftId: str, draft: DraftToPublish):
    service = ShotService(userId=userId)
    isDone = await service.publishDraft(draftId=draftId, draft=draft)
    return isDone

@router.get('/shot')
@cache(expire=60)
async def getShot(userId: str, shotId: str):
    service = ShotService(userId=userId)
    shot = await service.getShot(shotId=shotId)
    return shot
