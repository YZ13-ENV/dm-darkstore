from typing import List, Optional
from database.shot import getAllUsersShots, getShots, getDrafts, updateDraft, publishDraft, getShot
from schemas.draft import DraftShotData
from schemas.shot import ImageBlock, ShotDataForUpload

class ShotService():
    def __init__(self, userId: Optional[str] ):
        self.__userId = userId

    async def getShots(self, asDoc: bool):
        if (self.__userId):
            shots = await getShots(self.__userId, asDoc)
            return shots
        else:
            return None

    async def getShot(self, shotId: str):
        if self.__userId:
            shot = await getShot(self.__userId, shotId)
            return shot
        else:
            return None

    async def getDrafts(self, asDoc: bool):
        if (self.__userId):
            drafts = await getDrafts(self.__userId, asDoc)
            return drafts
        else:
            return None
        
    async def updateDraft(self, draftId: str, draft: ShotDataForUpload):
        isComplete = await updateDraft(userId=self.__userId, draftId=draftId, draft=draft)
        return isComplete

    async def publishDraft(self, draftId: str, draft: DraftShotData, needFeedBack: bool, tags: List[str], thumbnail: Optional[ImageBlock]):
        isDone = await publishDraft(userId=self.__userId, draftId=draftId, draft=draft, needFeedBack=needFeedBack, tags=tags, thumbnail=thumbnail)
        return isDone

    async def getAllUsersShots(self):
        shots = await getAllUsersShots()
        return shots