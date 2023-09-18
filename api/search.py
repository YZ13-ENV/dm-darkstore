from typing import List, Optional
from fastapi import APIRouter
from database.search_history import add_in_history
from database.shot import getAllShots, getCreatedDate, getViews
from helpers.searcher import createEventSearchQuery, createNoteSearchQuery, createShotSearchQuery, divide_chunks, getSearchedEvents, getSearchedNotes, getSearchedShots, shotSearcher
from schemas.shot import DocShotData
from fastapi_cache.decorator import cache
from firebase import db
from firebase_admin.firestore import firestore

router = APIRouter(
    prefix='/search',
    tags=['Поиск']
)

@router.get('/global')
@cache(expire=60)
async def globalSearch(userId: str, q: str):
    shots = await getSearchedShots(userId=userId, q=q.lower())
    chunkedShots = divide_chunks(shots, 3)
    shotsQueries = await createShotSearchQuery(userId=userId, list=chunkedShots)

    events = await getSearchedEvents(userId=userId, q=q.lower())
    eventQueries = await createEventSearchQuery(userId=userId, list=events)

    notes = await getSearchedNotes(userId=userId, q=q.lower())
    notesQueries = await createNoteSearchQuery(userId=userId, list=notes)
    allQueries = [ *notesQueries, *eventQueries, *shotsQueries ]

    return allQueries

@router.get('/shots')
# @cache(expire=60)
async def searchShots(q: str, order: str='popular', skip: Optional[int]=0, userId: Optional[str]=None):
    shots: List[DocShotData] = await getAllShots(skip=skip, order=order)
    res_shots = shotSearcher(q=q, shots=shots)
    if userId:
        await add_in_history(userId=userId, historyQuery=q)
    return res_shots

@router.delete('/{service}')
async def deleteSearchQuery(service: str, userId: str, queryId: str):
    try:
        queryRef: firestore.DocumentReference = db.collection('users').document(userId).collection('history').document('search').collection(service).document(queryId)
        await queryRef.delete()
        return True
    except:
        return False

@router.get('/{service}')
async def getSearchQuery(service: str, userId: str):
    queries: firestore.CollectionReference = db.collection('users').document(userId).collection('history').document('search').collection(service)
    allQr: List[firestore.DocumentSnapshot] = await queries.get()
    res = []
    for qr in allQr:
        qrDict = qr.to_dict()
        qrDict.update({ 'queryId': qr.id })
        res.append(qrDict)
    return res