from typing import Optional
from database.shot import getAllUsersShots, getShots, getDrafts

class ShotService():
    def __init__(self, userId: Optional[str] ):
        self.__userId = userId

    async def getShots(self, asDoc: bool):
        if (self.__userId):
            shots = await getShots(self.__userId, asDoc)
            return shots
        else:
            return None

    async def getDrafts(self, asDoc: bool):
        if (self.__userId):
            drafts = await getDrafts(self.__userId, asDoc)
            return drafts
        else:
            return None
        
    async def getAllUsersShots(self):
        shots = await getAllUsersShots()
        return shots