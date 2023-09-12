from typing import List, Optional
from fastapi import APIRouter
from database.shot import getAllShots, getCreatedDate, getViews
from helpers.searcher import createEventSearchQuery, createNoteSearchQuery, createShotSearchQuery, divide_chunks, getSearchedEvents, getSearchedNotes, getSearchedShots, shotSearcher
from schemas.shot import DocShotData

router = APIRouter(
    prefix='/search',
    tags=['Поиск']
)

@router.get('/global')
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
async def searchShots(q: str, order: str='popular', skip: Optional[int]=0):
    shots: List[DocShotData] = await getAllShots(skip=skip, order=order)
    res_shots = []

    for shot in shots:
        title: str = shot.get('title')
        tags: List[str] = shot.get('tags')
        if (q in title.lower()) or (q in tags):
            res_shots.append(shot)
        else:
            for block in shot['blocks']:
                text: Optional[str] = block.get('text')
                if text != None and q in text.lower():
                    res_shots.append(shot)
    res = []
    [res.append(x) for x in res_shots if x not in res]
    return res
