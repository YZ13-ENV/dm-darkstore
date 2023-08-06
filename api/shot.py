from typing import List, Optional
from schemas.draft import DraftShotData
from schemas.shot import ImageBlock, ShotDataForUpload
from services.shotService import ShotService
from fastapi import APIRouter
router = APIRouter(
    prefix='/shots',
    tags=['Работы']
)

@router.get('/onlyShots')
async def getOnlyShots(userId: str, asDoc: bool=True):
    service = ShotService(userId=userId)
    shots = await service.getShots(asDoc=asDoc)
    return shots

@router.get('/onlyDrafts')
async def getOnlyDrafts(userId: str, asDoc: bool=True):
    service = ShotService(userId=userId)
    drafts = await service.getDrafts(asDoc=asDoc)
    return drafts

@router.get('/allShots')
async def getAllShots():
    service = ShotService(userId=None)
    shots = await service.getAllUsersShots()
    return shots

@router.post('/updateDraft')
async def updateDraft(userId: str, draftId: str, draft: ShotDataForUpload):
    service = ShotService(userId=userId)
    isDone = await service.updateDraft(draftId, draft=draft)
    return isDone

@router.post('/publishDraft')
async def publishDraft(userId: str, draftId: str, draft: DraftShotData, needFeedBack:bool=True, tags: List[str]=[], thumbnail: Optional[ImageBlock]=None):
    service = ShotService(userId=userId)
    isDone = await service.publishDraft(draftId=draftId, draft=draft, needFeedBack=needFeedBack, tags=tags, thumbnail=thumbnail)
    return isDone