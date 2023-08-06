from pydantic import BaseModel
from typing import Union
from schemas.shot import ImageBlock, TextBlock, ShotGridBlock


class DraftShotData(BaseModel):
    isDraft: bool
    authorId: str
    title: str
    rootBlock: ImageBlock
    blocks: Union[TextBlock, ShotGridBlock, ImageBlock]
    createdAt: int

    class Config: 
        orm_mode = True