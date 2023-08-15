from typing import List, Optional
from database.shot import addOrRemoveLike, addView, getAllUsersShots, getShots, getDrafts, updateDraft, publishDraft, getShot, updateShot, getUpgradedUsersShots
from schemas.draft import DraftToPublish
from schemas.shot import ShotData, ShotDataForUpload

class ShotService():
    def __init__(self, userId: Optional[str] ):
        self.__userId = userId

    async def getShots(self, asDoc: bool, limit: Optional[int]=None):
        if (self.__userId):
            shots = await getShots(self.__userId, asDoc=asDoc, limit=limit)
            return shots
        else:
            return None

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
        # try:
            isComplete = await updateShot(self.__userId, shotId, shot)
            return isComplete
        # except: 
            # return False

    async def updateDraft(self, draftId: str, draft: ShotDataForUpload):
        isComplete = await updateDraft(userId=self.__userId, draftId=draftId, draft=draft)
        return isComplete

    async def publishDraft(self, draftId: str, draft: DraftToPublish):
        isDone = await publishDraft(userId=self.__userId, draftId=draftId, draft=draft)
        return isDone

    async def getAllUsersShots(self, order: str):
        shots = await getAllUsersShots(order=order, userId=self.__userId)
        return shots
    
    async def getAllUpgradedUsersShots(self, order: str):
        shots = await getUpgradedUsersShots(order=order, userId=self.__userId)
        return shots