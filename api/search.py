from typing import List
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
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
        if q in shot['title'] or q in shot['blocks']:
            res_shots.append(shot)
        else:
            for block in shot['blocks']:
                if q in block.get('text'):
                    res_shots.append(shot)

    return res_shots