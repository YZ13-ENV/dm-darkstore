from typing import List, Optional
from fastapi import APIRouter
from database.shot import getAllShots
from schemas.shot import DocShotData

router = APIRouter(
    prefix='/search',
    tags=['Поиск']
)

@router.get('/shots')
async def searchShots(q: str):
    shots: List[DocShotData] = await getAllShots()
    res_shots = []

    for shot in shots:
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