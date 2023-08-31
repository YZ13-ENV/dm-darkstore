
from typing import Union
from pydantic import BaseModel


class CalendarEvent(BaseModel):
    key: str
    title: str
    description: str
    startDate: Union[int, float]
    endDate: Union[int, float]

    class Config: 
        orm_mode = True

class DocCalendarEvent(BaseModel):
    doc_id: str
    key: str
    title: str
    description: str
    startDate: Union[int, float]
    endDate: Union[int, float]

    class Config: 
        orm_mode = True