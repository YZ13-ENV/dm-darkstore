from database.shot import getShots, getDrafts

class ShotService():
    def __init__(self, userId: str):
        self.__userId = userId

    async def getShots(self, asDoc: bool):
        shots = await getShots(self.__userId, asDoc)
        return shots

    async def getDraft(self, asDoc: bool):
        drafts = await getDrafts(self.__userId, asDoc)
        return drafts