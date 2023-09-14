from pydantic import BaseModel
from typing import Optional, Union, List
from schemas.shot import MediaBlock, TextBlock, ShotGridBlock, Thumbnail

class DraftShotData(BaseModel):
    isDraft: bool
    authorId: str
    title: str
    rootBlock: MediaBlock
    blocks: List[Union[TextBlock, ShotGridBlock, MediaBlock]]
    thumbnail: Optional[Thumbnail]
    createdAt: Union[int, float]

    class Config: 
        orm_mode = True

class DraftToPublish(BaseModel):
    isDraft: bool
    enableMdSyntax: bool
    authorId: str
    title: str
    rootBlock: MediaBlock
    blocks: List[Union[TextBlock, ShotGridBlock, MediaBlock]]
    createdAt: Union[int, float]
    tags: List[str]
    needFeedback: bool
    thumbnail: Optional[Thumbnail]

    class Config: 
        orm_mode = True