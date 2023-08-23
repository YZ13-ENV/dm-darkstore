from pydantic import BaseModel
from typing import Optional, List, Union

class Session(BaseModel):
    sid: str
    uid: Optional[str]
    uids: List[Union[None, str]]

    class Config: 
        orm_mode = True