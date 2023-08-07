from fastapi import Response
from jwt import encode
import dotenv

from typing import Optional

from database.user import getUserUIDByEmail


class AuthService():
    def __init__(self, userId: Optional[str]= None) -> None:
        self.__userId = userId




    async def getSignOut(self, res: Response):
        res.delete_cookie('uid')
        return res


    async def returnAuthoredUser(self, res: Response, email: str):
        dotenv.load_dotenv()
        uid = await getUserUIDByEmail(email)
        if uid:
            secret = dotenv.get_key('.env', 'JWT_SECRET')
            if secret:
                decoded_uid = encode({ 'uid': uid }, secret, algorithm='HS256')
                res.set_cookie('uid', decoded_uid, secure=True)
                return res
            return None
        else:
            return None