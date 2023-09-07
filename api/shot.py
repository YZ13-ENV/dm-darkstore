from typing import List, Optional
from schemas.draft import  DraftToPublish
from schemas.shot import CommentBlock, NewCommentBlock, ShotData, ShotDataForUpload
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
async def getOnlyShots(userId: str, asDoc: bool=True, order: Optional[str]='popular', limit: Optional[int]=None, exclude: Optional[str]=None):
    service = ShotService(userId=userId)
    shots = await service.getShots(asDoc=asDoc, limit=limit, exclude=exclude, order=order)
    return shots

@router.get('/onlyDrafts')
@cache(expire=60)
async def getOnlyDrafts(userId: str, asDoc: bool=True):
    service = ShotService(userId=userId)
    drafts = await service.getDrafts(asDoc=asDoc)
    return drafts

@router.get('/v2/allShots/{order}', deprecated=True)
@cache(expire=60)
async def getPopularFromAllShots(order: Optional[str]='popular', userId: Optional[str]=None):
    service = ShotService(userId=userId)
    shots = await service.getAllUpgradedUsersShots(order=order)
    return shots

@router.get('/allShotsCount')
async def getAllShotCount():
    group = db.collection_group('shots')
    shotsSnapsQuery = group.where('isDraft', '==', False)
    shots = await shotsSnapsQuery.get()
    list = []
    for shot in shots:
        shotDict = shot.to_dict()
        list.append(shotDict)
    return len(list)


@router.get('/v2/chunkedAllShots/{order}')
async def getChunkedShots(order: str='popular', userId: Optional[str]=None, skip: Optional[int]=0):
    service = ShotService(userId=userId)
    shots = await service.getChunk(order=order, skip=skip)

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
async def getShot(userId: str, shotId: str):
    service = ShotService(userId=userId)
    shot = await service.getShot(shotId=shotId)
    return shot

@router.post('/comment')
async def addComment(userId: str, shotId: str, comment: NewCommentBlock):
    service = ShotService(userId=userId)
    isAdded = await service.addComment(shotId=shotId, comment=comment)
    return isAdded

@router.patch('/comment')
async def patchComment(userId: str, shotId: str, comment: CommentBlock):
    service = ShotService(userId=userId)
    isPatched = await service.patchComment(shotId=shotId, comment=comment)
    return isPatched

@router.delete('/comment')
async def removeComment(userId: str, shotId: str, commentId: str):
    service = ShotService(userId=userId)
    isAdded = await service.removeComment(shotId=shotId, commentId=commentId)
    return isAdded

@router.delete('/shot')
async def deleteShot(userId: str, shotId: str):
    service = ShotService(userId=userId)
    res = await service.deleteShot(shotId=shotId)
    return res
