from typing import Optional, Union
from fastapi import APIRouter
from database.shot import getCreatedDate, getViews
from firebase import db
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix='/tags',
    tags=['Тэги']
)

@router.get('/{tag}/{order}')
@cache(expire=120)
async def getShotByTag(tag: str, order: str='popular', skip: Optional[int]=0):
    group = db.collection_group('shots')#.limit(16).offset(skip)
    q = group.where('tags', 'array_contains', tag)
    snaps = await q.get()

    order_by = getViews if order == 'popular' else getCreatedDate

    list = []
    for snap in snaps:
        snapDict = snap.to_dict()
        snapDict.update({ 'doc_id': snap.id })
        list.append(snapDict)

    list.sort(key=order_by if order != 'following' else getCreatedDate, reverse=True)

    return list