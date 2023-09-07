from typing import List, Optional
from database.user import getShortDataFromRecord
from firebase import db
from schemas.note import Note
from schemas.shot import ShotData
from schemas.event import CalendarEvent
def divide_chunks(l, n):
      
    for i in range(0, len(l), n): 
        yield l[i:i + n]

async def createShotSearchQuery(userId: str, list: List[List[ShotData]]):
    queries = []
    shortData = await getShortDataFromRecord(userId=userId)
    if shortData:
        for item in list:
            searchQuery = {
                'type': 'shots',
                'user': shortData.get('short'),
                'items': item
            }
            queries.append(searchQuery)
    return queries

async def getSearchedShots(userId: str, q: str):
    collRef = db.collection('users').document(userId).collection('shots')
    collSnaps = await collRef.get()
    shotSnaps = []
    for snap in collSnaps:
        snapDict = snap.to_dict()
        shotSnaps.append(snapDict)
    searchedSnaps = shotSearcher(q=q, shots=shotSnaps)
    return searchedSnaps

def shotSearcher(q: str, shots: List):
    res_shots = []

    for shot in shots:
        if not shot in res_shots:
            title: str = shot.get('title')
            if q in title.lower():
                res_shots.append(shot)
            else:
                for block in shot['blocks']:
                    text: Optional[str] = block.get('text')
                    if text != None:
                        if q in text.lower():
                            res_shots.append(shot)

    return res_shots

async def getSearchedEvents(userId: str, q: str):
    collRef = db.collection('users').document(userId).collection('events')
    collSnaps = await collRef.get()
    eventSnaps = []
    for snap in collSnaps:
        snapDict = snap.to_dict()
        eventSnaps.append(snapDict)
    searchedSnaps = await eventSearcher(q=q, events=eventSnaps)
    return searchedSnaps

async def eventSearcher(q: str, events: List):
    res_shots = []

    for event in events:
        title: str = event.get('title')
        description: str = event.get('description')
        if q in title.lower() or q in description.lower():
            res_shots.append(event)

    return res_shots

async def createEventSearchQuery(userId: str, list: List[CalendarEvent]):
    queries = []
    shortData = await getShortDataFromRecord(userId=userId)
    if shortData:
        for item in list:
            searchQuery = {
                'type': 'events',
                'user': shortData.get('short'),
                'items': item
            }
            queries.append(searchQuery)
    return queries


async def getSearchedNotes(userId: str, q: str):
    collRef = db.collection('users').document(userId).collection('notes')
    collSnaps = await collRef.get()
    noteSnaps = []
    for snap in collSnaps:
        snapDict = snap.to_dict()
        noteSnaps.append(snapDict)
    searchedSnaps = await noteSearcher(q=q, notes=noteSnaps)
    return searchedSnaps

async def noteSearcher(q: str, notes: List):
    res_shots = []

    for note in notes:
        title: str = note.get('title')
        if q in title.lower():
            res_shots.append(note)
        else:
            blocks = note.get('blocks')
            for block in blocks:
                if block.get('type') == 'text' or block.get('type') == 'heading':
                    text: str = block.get('text')
                    if q in text.lower():
                        res_shots.append(note)
                elif block.get('type') == 'task-list' or block.get('type') == 'list':
                    block_title: str = block.get('title')
                    if q in block_title.lower():
                        res_shots.append(note)

    return res_shots


async def createNoteSearchQuery(userId: str, list: List[Note]):
    queries = []
    shortData = await getShortDataFromRecord(userId=userId)
    if shortData:
        for item in list:
            searchQuery = {
                'type': 'notes',
                'user': shortData.get('short'),
                'items': item
            }
            queries.append(searchQuery)
    return queries
