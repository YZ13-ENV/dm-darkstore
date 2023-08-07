from typing import Dict, Any
from firebase import auth
from database.user import getShortDataByEmail, updateUser, getShortDataFromRecord

class UserService():
    def __init__(self, userId: str):
        self.__userId = userId

    async def getShortData(self):
        if (self.__userId):
            data: Dict[str, Any] = await getShortDataFromRecord(self.__userId)
            return data
        else:
            return None

    async def getShortDataByEmail(self, email: str):
        data = await getShortDataByEmail(email)
        return data

    async def generateCustomToken(self):
        if (self.__userId):
            token = auth.create_custom_token(self.__userId)
            return token
        else:
            return None
        
    async def updateUser(self, displayName: str, photoUrl: str):

        if (self.__userId):
            isComplete =  await updateUser(userId=self.__userId, displayName=displayName, photoUrl=photoUrl)
            return isComplete
        
        return False