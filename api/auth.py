import os
from typing import Dict, Union
from uuid import uuid4
from schemas.auth import Session
from services.authService import AuthService
from fastapi import APIRouter
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
async def getSession(sid: str):
    try:
        sidFromToken: Dict[str, str] = decode(sid, os.getenv('JWT_SECRET'))
        taken_sid = sidFromToken.get('sid')
        sessionRef = db.collection('sessions').document(taken_sid)
        sessionSnap = await sessionRef.get()
        sessionDict = sessionSnap.to_dict()
        payload = {
            'session': sessionDict
        }
        token: str = encode(payload=payload, key=os.getenv('JWT_SECRET'))
        return token
    except:
        return None

@router.post('/generate/session')
async def generateSession():
    session: Session = {
        'sid': uuid4(),
        'uid': None,
        'disabled': False,
        'uids': []
    }
    payload = {
        'session': session
    }
    token: str = encode(payload=payload, key=os.getenv('JWT_SECRET'))
    return token


@router.post('/generate/sid')
async def generateSessionSid(sid: str):
    payload = {
        'sid': sid
    }
    token: str = encode(payload=payload, key=os.getenv('JWT_SECRET'))
    return token
