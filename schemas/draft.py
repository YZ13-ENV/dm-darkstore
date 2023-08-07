from pydantic import BaseModel
from typing import Optional, Union, List
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


class DraftToPublish(BaseModel):
    isDraft: bool
    authorId: str
    title: str
    rootBlock: ImageBlock
    blocks: List[Union[TextBlock, ShotGridBlock, ImageBlock]]
    createdAt: Union[int, float]
    tags: List[str]
    needFeedBack: bool
    thumbnail: Optional[ImageBlock]

    class Config: 
        orm_mode = True