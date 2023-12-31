from typing import List, Optional, Union
from helpers.nickname import getUidByNickName
from schemas.draft import  DraftToPublish
from schemas.shot import CommentBlock, NewCommentBlock, ShotData, ShotDataForUpload
from services.shotService import ShotService
from fastapi import APIRouter
from fastapi_cache.decorator import cache
from database.shot import chunkUserWithOrder, chunkWithOrder, chunkWithOrderAndCategory, getShot
from fastapi_cache import FastAPICache

router = APIRouter(
    prefix='/shots',
    tags=['Работы']
)

@router.get('/onlyShots/{nickname}')
@cache(namespace='shots', expire=60)
async def getOnlyShots(nickname: str, order: Optional[str]='popular', limit: Optional[int]=None, exclude: Optional[str]=None):
    userId: Union[str, None] = await getUidByNickName(nickname=nickname)
    if userId:
        service = ShotService(userId=userId)
        shots = await service.getShots(limit=limit, exclude=exclude, order=order)
        return shots
    else:
        return None

@router.get('/onlyDrafts/{nickname}')
@cache(namespace='shots', expire=60)
async def getOnlyDrafts(nickname: str, asDoc: bool=True):
    userId: Union[str, None] = await getUidByNickName(nickname=nickname)
    if userId:
        service = ShotService(userId=userId)
        drafts = await service.getDrafts(asDoc=asDoc)
        return drafts
    else:
        return None

@router.get('/all/{order}')
@cache(namespace='shots', expire=60)
async def getSomeShots(order: str='popular', skip: Optional[str]=None):
    shots = await chunkWithOrder(order=order, skip=int(skip))
    return shots

@router.get('/all/{order}/{category}')
@cache(namespace='shots', expire=60)
async def getSomeShotsWithCategories(order: str='popular', category: Optional[str]=None, skip: Optional[str]=None):
    shots = await chunkWithOrderAndCategory(order=order, category=category, skip=int(skip))
    return shots

@router.get('/user/{nickname}/{order}')
@cache(namespace='shots', expire=60)
async def getUserShots(nickname: str, order: str='popular', skip: Optional[str]=None):
    userId: Union[str, None] = await getUidByNickName(nickname=nickname)
    if userId:
        shots = await chunkUserWithOrder(order=order, userId=userId, skip=int(skip))
        return shots
    else:
        return None

@router.get('/count/{order}')
@cache(namespace='shots', expire=60)
async def getSomeShotsCount(order: str='popular'):
    count = await chunkWithOrder(order=order, skip=None)
    return count

@router.get('/count/{order}/{category}')
@cache(namespace='shots', expire=60)
async def getSomeShotsCountWithCategories(category: str, order: str='popular'):
    count = await chunkWithOrderAndCategory(order=order, category=category, skip=None)
    return count

@router.get('/user/count/{nickname}/{order}')
@cache(namespace='shots', expire=60)
async def getUserShots(nickname: str, order: str='popular'):
    userId: Union[str, None] = await getUidByNickName(nickname=nickname)
    if userId:
        count = await chunkUserWithOrder(order=order, userId=userId, skip=None)
        return count
    else:
        return None

@router.post('/updateShot')
async def updateShot(userId: str, shotId: str, shot: ShotData):
    service = ShotService(userId=userId)
    isDone = await service.updateShot(shotId=shotId, shot=shot)
    return isDone

@router.get('/shot/{shotId}')
@cache(namespace='shots', expire=60)
async def getShotWithShotId(shotId: str):
    shot = await getShot(shotId=shotId)
    return shot

@router.get('/shot/{shotId}/{userId}')
@cache(namespace='shots', expire=60)
async def getShotWithUserIdAndShotId(userId: str, shotId: str):
    shot = await getShot(userId=userId, shotId=shotId)
    return shot

@router.post('/updateDraft')
async def updateDraft(userId: str, draftId: str, draft: ShotDataForUpload):
    service = ShotService(userId=userId)
    isDone = await service.updateDraft(draftId, draft=draft)
    return isDone

@router.post('/publishDraft')
async def publishDraft(userId: str, draftId: str, draft: DraftToPublish):
    service = ShotService(userId=userId)
    isDone = await service.publishDraft(draftId=draftId, draft=draft)
    await FastAPICache.clear('shots')
    return isDone

@router.post('/comment')
async def addComment(userId: str, shotId: str, comment: NewCommentBlock):
    service = ShotService(userId=userId)
    isAdded = await service.addComment(shotId=shotId, comment=comment)
    return isAdded

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

# @router.delete('/shot/{shotId}')
# @router.delete('/shot/{shotId}/{userId}')
@router.delete('/shot/{shotId}/{userId}')
async def deleteShot(userId: str, shotId: str):
    service = ShotService(userId=userId)
    res = await service.deleteShot(shotId=shotId)
    return res
