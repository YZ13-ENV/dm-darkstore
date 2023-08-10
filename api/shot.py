from typing import Optional
from schemas.draft import  DraftToPublish
from schemas.shot import ShotData, ShotDataForUpload
from services.shotService import ShotService
from fastapi import APIRouter
router = APIRouter(
    prefix='/shots',
    tags=['Работы']
)

@router.get('/onlyShots')
async def getOnlyShots(userId: str, asDoc: bool=True, limit: Optional[int]=None):
    service = ShotService(userId=userId)
    shots = await service.getShots(asDoc=asDoc, limit=limit)
    return shots

@router.get('/onlyDrafts')
async def getOnlyDrafts(userId: str, asDoc: bool=True):
    service = ShotService(userId=userId)
    drafts = await service.getDrafts(asDoc=asDoc)
    return drafts

@router.get('/allShots')
async def getAllShots():
    # popular default if auth == None | following = default if auth !== None | new
    service = ShotService(userId=None)
    shots = await service.getAllUsersShots()
    return shots

@router.post('/updateShot')
async def updateDraft(userId: str, shotId: str, shot: ShotData):
    service = ShotService(userId=userId)
    isDone = await service.updateShot(shotId=shotId, shot=shot)
    return isDone

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
async def getShot(userId: str, shotId: str):
    service = ShotService(userId=userId)
    shot = await service.getShot(shotId=shotId)
    return shot