import os
import jwt
import datetime
from firebase_admin import firestore
from firebase import db
from typing import List, Union
from fastapi import APIRouter, Header

from database.user import setPlusSubscription
from helpers.generators import id_generator


router = APIRouter(
    prefix='/plus',
    tags=['Подписка']
)

@router.get('/code/{code}')
async def checkCode(code: str):
    codesRef: firestore.firestore.AsyncCollectionReference = db.collection('dm').document('global').collection('promocodes')
    codes = await codesRef.get()
    targetCode = None
    for pCode in codes:
        codeDict = pCode.to_dict()
        if codeDict.get('code') == code:
            targetCode = codeDict
            targetCode.update({ 'id': pCode.id })
    return targetCode

@router.delete('/code/{code}')
async def removeCode(code: str, token: Union[str, None] = Header(default=None)):
    if (token):
        tokenData = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'], options={"verify_iat":False})
        verifyToken = tokenData.get('verifyToken')
        if (verifyToken == os.getenv('TOKEN')):
            codesRef: firestore.firestore.AsyncCollectionReference = db.collection('dm').document('global').collection('promocodes')
            codes: List[firestore.firestore.DocumentSnapshot] = await codesRef.get()
            idToDelete = None
            for pCode in codes:
                codeDict = pCode.to_dict()
                if codeDict.get('code') == code:
                    idToDelete = pCode.id
            if (idToDelete):
                codeDocRef = codesRef.document(idToDelete)
                await codeDocRef.delete()
                return True
        else:
            return False
    else:
        return False

@router.post('/create/code')
async def generateCode(token: Union[str, None] = Header(default=None)):
    try:
        if (token):
            tokenData = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'], options={"verify_iat":False})
            verifyToken = tokenData.get('verifyToken')
            codesRef: firestore.firestore.AsyncCollectionReference = db.collection('dm').document('global').collection('promocodes')
            newCode = {
                'code': id_generator(10),
                'expiredAt': (datetime.datetime.now() + datetime.timedelta(days=7)).timestamp()
            }
            if (verifyToken == os.getenv('TOKEN')): 
            	await codesRef.add(newCode)
            	return True
            else:
                return False	
        else:
            return False
    except:
        return False

@router.post('/setSubStatus')
async def setSubStatus(userId: str, status: bool=False, token: Union[str, None] = Header(default=None)):
    try:
        if (token):
            tokenData = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'], options={"verify_iat":False})
            iat = tokenData.get('iat')
            verifyToken = tokenData.get('verifyToken')
            now = datetime.datetime.now().timestamp()
            if (now > iat or not iat or verifyToken != os.getenv('TOKEN')):
                return None
            else: 
                res = await setPlusSubscription(userId=userId, subscriptionStatus=status)
                return res
        else:
            return None
    except:
        return None

@router.get('/accessToSub')
async def getAccessToSub(token: Union[str, None] = Header(default=None)):
    try:
        if (token):
            tokenData = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'], options={"verify_iat":False})
            iat = tokenData.get('iat')
            verifyToken = tokenData.get('verifyToken')
            now = datetime.datetime.now().timestamp()
            if (now > iat or not iat or verifyToken != os.getenv('TOKEN')):
                return None
            else: 
                tokenPayload = {
                    'iat': (datetime.datetime.now() + datetime.timedelta(minutes=5)).timestamp(),
                    'verifyToken': os.getenv('TOKEN')
                }
                return jwt.encode(tokenPayload, os.getenv('JWT_SECRET'), algorithm='HS256')
        else:
            return None
    except:
        return None
