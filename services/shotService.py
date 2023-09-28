from typing import Optional
from database.shot import addComment, addOrRemoveLike, addView, getShots, getDrafts, getUserChunkedShots, patchComment, removeComment, updateDraft, publishDraft, getShot, updateShot, getUpgradedUsersShots, getDeleteShot, getChunkedShots
from schemas.draft import DraftToPublish
from schemas.shot import CommentBlock, NewCommentBlock, ShotData, ShotDataForUpload

class ShotService():
    def __init__(self, userId: Optional[str] ):
        self.__userId = userId

    async def getShots(self, limit: Optional[int]=None, exclude: Optional[str]=None, order: Optional[str]='popular'):
        if (self.__userId):
            shots = await getShots(userId=self.__userId, limit=limit, exclude=exclude, order=order)
            return shots
        else:
            return None

    async def getChunk(self, order: str, skip: Optional[int]):
        shots = await getChunkedShots(order=order, userId=self.__userId, skip=skip)
        return shots
    
    async def getUserChunk(self, order: str, skip: Optional[int]):
        if self.__userId:
            shots = await getUserChunkedShots(userId=self.__userId, order=order, skip=skip)
            return shots
        else: return []

    async def getShot(self, shotId: str):
        if self.__userId:
            shot = await getShot(self.__userId, shotId)
            return shot
        else:
            return None

    async def addOrRemoveLikes(self, shotId: str, uid: str):
        if (self.__userId):
            result = await addOrRemoveLike(shotAuthorId=self.__userId, shotId=shotId, uid=uid)
            return result
        else:
            return None

    async def addView(self, shotId: str, uid: str):
        if (self.__userId):
            result = await addView(shotAuthorId=self.__userId, shotId=shotId, uid=uid)
        else:
            return None

    async def getDrafts(self, asDoc: bool):
        if (self.__userId):
            drafts = await getDrafts(self.__userId, asDoc)
            return drafts
        else:
            return None
    
    async def updateShot(self, shotId: str, shot: ShotData):
            if self.__userId:
                isComplete = await updateShot(self.__userId, shotId, shot)
                return isComplete
            else:
                return False
    async def updateDraft(self, draftId: str, draft: ShotDataForUpload):
        if self.__userId:
            isComplete = await updateDraft(userId=self.__userId, draftId=draftId, draft=draft)
            return isComplete
        else:
            return False

    async def publishDraft(self, draftId: str, draft: DraftToPublish):
        if self.__userId:
            isDone = await publishDraft(userId=self.__userId, draftId=draftId, draft=draft)
            return isDone
        else:
            return False

    async def getAllUpgradedUsersShots(self, order: Optional[str]):
        shots = await getUpgradedUsersShots(order=order, userId=self.__userId)
        return shots

    async def deleteShot(self, shotId: str):
        if (self.__userId):
            res = await getDeleteShot(self.__userId, shotId)
            return res
        else:
            return False

    async def addComment(self, shotId: str, comment: NewCommentBlock):
        if self.__userId:
            isAdded = await addComment(userId=self.__userId, shotId=shotId, comment=comment)
            return isAdded
        else: return False

    async def patchComment(self, shotId: str, comment: CommentBlock):
        if self.__userId:
            isPatched = await patchComment(userId=self.__userId, shotId=shotId, comment=comment)
            return isPatched
        else: return False

    async def removeComment(self, shotId: str, commentId: str):
        if self.__userId:
            isAdded = await removeComment(userId=self.__userId, shotId=shotId, commentId=commentId)
            return isAdded
        else: return False