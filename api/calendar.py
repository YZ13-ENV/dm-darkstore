from fastapi import APIRouter
from firebase import db
from schemas.event import CalendarEvent


router = APIRouter(
    prefix='/calendar',
    tags=['События']
)

@router.post('/event')
async def postEvent(userId: str, event: CalendarEvent):
    try:
        eventRef = db.collection('users').document(userId).collection('events')
        eventDict = event.dict()
        await eventRef.add(eventDict)
        return True
    except:
        return False