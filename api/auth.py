import os
from typing import Dict, Union
from schemas.auth import Session
from services.authService import AuthService
from fastapi import APIRouter, Response
from fastapi.responses import Response
from firebase import db
from jwt import decode, encode
router = APIRouter(
    prefix='/auth',
    tags=['Авторизация']
)

@router.post('/authComplete')
async def authComplete(email: str):
    service = AuthService()
    uid: Union[str, None] = await service.returnAuthoredUser(email=email)
    if not uid:
        res = Response(status_code=200)
        return res
    else:
        res = Response(status_code=200)
        res['accessToken'] = uid
        return res


@router.get('/session')
async def postSession(sid: str):
    try:
        sidFromToken: Dict[str, str] = decode(sid, os.getenv('JWT_SECRET'))
        taken_sid = sidFromToken.get('sid')
        sessionRef = db.collection('sessions').document(taken_sid)
        sessionSnap = await sessionRef.get()
        sessionDict = sessionSnap.to_dict()
        return sessionDict
    except:
        return None

@router.post('/session')
async def postSession(sessionToken: str):
    try:
        sessionFromToken = Dict[str, str] = decode(sessionToken, os.getenv('JWT_SECRET'))
        sessionDict = sessionFromToken.get('session')
        sessionRef = db.collection('sessions').document(sessionDict.get('sid'))
        sessionSnap = await sessionRef.get()
        if sessionSnap.exists:
            await sessionRef.update(sessionDict)
            return True
        else:
            await sessionRef.set(sessionDict)
            return True
    except: 
        return False