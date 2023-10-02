from typing import List, Optional
from database.user import getFollows
from helpers.shots_categories import getCategory
from schemas.draft import  DraftToPublish
from schemas.shot import CommentBlock, NewCommentBlock, ShotData, ShotDataForUpload
from services.shotService import ShotService
from fastapi import APIRouter
from fastapi_cache.decorator import cache
from firebase import db
from database.shot import getChunkByCategory, getChunkedShotsWithRecommendations, getShotById
router = APIRouter(
    prefix='/shots',
    tags=['Работы']
)

@router.get('/onlyShots')
@cache(expire=60)
async def getOnlyShots(userId: str, order: Optional[str]='popular', limit: Optional[int]=None, exclude: Optional[str]=None):
    service = ShotService(userId=userId)
    shots = await service.getShots(limit=limit, exclude=exclude, order=order)
    return shots

@router.get('/onlyDrafts')
@cache(expire=60)
async def getOnlyDrafts(userId: str, asDoc: bool=True):
    service = ShotService(userId=userId)
    drafts = await service.getDrafts(asDoc=asDoc)
    return drafts

@router.get('/allShotsCount/{order}')
@cache(expire=60)
async def getAllShotCount(userId: Optional[str]=None, order: str='popular'):
    group = db.collection_group('shots')
    shotsSnapsQuery = group.where('isDraft', '==', False)
    
    if userId and order == 'following':
        follows = await getFollows(userId=userId)
        shotsSnapsQuery = group.where('isDraft', '==', False).where('authorId', 'in', follows)

    shots = await shotsSnapsQuery.get()
    list = []

    for shot in shots:
        shotDict = shot.to_dict()
        list.append(shotDict)

    return len(list)
@router.get('/v2/chunkByCategoriesCount/{category}/{order}')
@cache(expire=60)
async def chunkByCategoriesCount(category: str, order: str='popular', skip: Optional[int]=0):
    category_tags = await getCategory(category)
    if category_tags:
        shots = await getChunkByCategory(order=order, skip=skip, tags=category_tags)
        return len(shots)
    return 0
@router.get('/v2/chunkByCategories/{category}/{order}')
@cache(expire=60)
async def getChunkByCategories(category: str, order: str='popular', skip: Optional[int]=0):
    category_tags = await getCategory(category)
    if category_tags:
        shots = await getChunkByCategory(order=order, skip=skip, tags=category_tags)
        return shots
    return None

@router.get('/v2/chunkWithRecommendationsCount/{order}')
@cache(expire=60)
async def getChunkWithRecommendations(userId: str, order: str='popular', skip: Optional[int]=0):
    shots = await getChunkedShotsWithRecommendations(order=order, skip=skip, userId=userId)
    return len(shots)

@router.get('/v2/chunkWithRecommendations/{order}')
@cache(expire=60)
async def getChunkWithRecommendations(userId: str, order: str='popular', skip: Optional[int]=0):
    shots = await getChunkedShotsWithRecommendations(order=order, skip=skip, userId=userId)
    return shots

@router.get('/userShotsCount/{userId}')
@cache(expire=60)
async def getAllUserShotsCount(userId: str):
    userShotsRef = db.collection('users').document(userId).collection('shots')
    shots = await userShotsRef.get()
    count = len(shots)
    return count

@router.get('/v2/chunkedUserShots/{order}')
@cache(expire=60)
async def getUserChunkedShots(userId: str, order: str='popular', skip: Optional[int]=0):
    service = ShotService(userId=userId)
    shots = await service.getUserChunk(order=order, skip=skip)
    return shots

@router.get('/v2/chunkedAllShots/{order}')
@cache(expire=60)
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

@router.get('/shotById')
# @cache(expire=60)
async def getShot(shotId: str):
    shot = await getShotById(shotId=shotId)
    return shot

@router.get('/shot')
@cache(expire=60)
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
