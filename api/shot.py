from fastapi import APIRouter
from services.shotService import ShotService
router = APIRouter(
    prefix='/shots',
    tags=['Работы']
)

@router.get('/onlyShots')
async def getOnlyShots(userId: str, asDoc: bool=True):
    service = ShotService(userId=userId)
    shots = await service.getShots(asDoc=asDoc)
    return shots

@router.get('/onlyDrafts')
async def getOnlyDrafts(userId: str, asDoc: bool=True):
    service = ShotService(userId=userId)
    drafts = await service.getDrafts(asDoc=asDoc)
    return drafts

@router.get('/allShots')
async def getAllShots():
    service = ShotService(userId=None)
    shots = await service.getAllUsersShots()
    return shots