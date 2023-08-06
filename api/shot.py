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