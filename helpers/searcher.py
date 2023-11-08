from typing import List, Optional
from database.user import getShortDataFromRecord
from firebase import db
from schemas.shot import ShotData
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
            tags: List[str] = shot.get('tags')
            if q in title.lower():
                res_shots.append(shot)
            elif q in tags:
                res_shots.append(shot)
            else:
                for block in shot['blocks']:
                    text: Optional[str] = block.get('text')
                    if text != None:
                        if q in text.lower():
                            res_shots.append(shot)

    return res_shots
