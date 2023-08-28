from typing import Union
from fastapi import APIRouter
from firebase import db
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix='/tags',
    tags=['Тэги']
)

@router.get('/{tag}')
@cache(expire=120)
async def getShotByTag(tag: str, sortBy: str='popular'):
    group = db.collection_group('shots')
    list = []
    if sortBy == 'popular':
        q = group.where('tags', 'array_contains', tag).order_by(field_path='views', direction='DESCENDING')
        snaps = await q.get()

        for snap in snaps:
            snapDict = snap.to_dict()
            snapDict.update({ 'doc_id': snap.id })
            list.append(snapDict)

        return list
    elif sortBy == 'new':
        q = group.where('tags', 'array_contains', tag).order_by(field_path='createdAt', direction='DESCENDING')
        snaps = await q.get()

        for snap in snaps:
            snapDict = snap.to_dict()
            snapDict.update({ 'doc_id': snap.id })
            list.append(snapDict)

        return list
    
    else:
        q = group.where('tags', 'array_contains', tag)
        snaps = await q.get()

        for snap in snaps:
            snapDict = snap.to_dict()
            snapDict.update({ 'doc_id': snap.id })
            list.append(snapDict)

        return list