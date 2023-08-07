from pydantic import BaseModel
from typing import Union, List
from schemas.shot import ImageBlock, TextBlock, ShotGridBlock


class DraftShotData(BaseModel):
    isDraft: bool
    authorId: str
    title: str
    rootBlock: ImageBlock
    blocks: List[Union[TextBlock, ShotGridBlock, ImageBlock]]
    createdAt: Union[int, float]

    class Config: 
        orm_mode = True