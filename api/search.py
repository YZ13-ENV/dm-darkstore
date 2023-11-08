from typing import List, Optional
from fastapi import APIRouter
from database.search_history import add_in_history
from database.shot import getAllShots, getCreatedDate, getViews
from helpers.searcher import shotSearcher
from schemas.shot import DocShotData
from fastapi_cache.decorator import cache
from firebase import db
from firebase_admin.firestore import firestore

router = APIRouter(
    prefix='/search',
    tags=['Поиск']
)


@router.get('/query/{q}/{order}')
@cache(expire=60)
async def searchShots(q: str, order: str='popular', userId: Optional[str]=None):
    shots: List[DocShotData] = await getAllShots()
    order_by = getViews if order == 'popular' else getCreatedDate
    res_shots = shotSearcher(q=q, shots=shots)
    if userId:
        await add_in_history(userId=userId, historyQuery=q)
    res_shots.sort(key=order_by, reverse=True)
    return res_shots

@router.delete('/history/{service}')
async def deleteSearchQuery(service: str, userId: str, queryId: str):
    try:
        queryRef: firestore.DocumentReference = db.collection('users').document(userId).collection('history').document('search').collection(service).document(queryId)
        await queryRef.delete()
        return True
    except:
        return False

@router.get('/history/{service}')
async def getSearchQuery(service: str, userId: str):
    queries: firestore.CollectionReference = db.collection('users').document(userId).collection('history').document('search').collection(service)
    allQr: List[firestore.DocumentSnapshot] = await queries.get()
    res = []
    for qr in allQr:
        qrDict = qr.to_dict()
        qrDict.update({ 'queryId': qr.id })
        res.append(qrDict)
    return res