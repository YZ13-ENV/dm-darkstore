from typing import Dict
from database.user import getShortData

class UserService():
    def __init__(self, userId: str):
        self.__userId = userId

    async def getShortData(self):
        if (self.__userId):
            data: Dict[str, Any] = await getShortData(self.__userId)
            return data
        else:
            return None
