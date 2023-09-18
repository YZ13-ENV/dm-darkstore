from typing import Union
from pydantic import BaseModel


class HistorySearchQuery(BaseModel):
    query: str
    createdAt: Union[int, float]

    class Config: 
        orm_mode = True

class HistorySearchQueryWithID(BaseModel):
    queryId: str
    query: str
    createdAt: Union[int, float]

    class Config: 
        orm_mode = True