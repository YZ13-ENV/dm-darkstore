from pydantic import BaseModel
from typing import Optional, Union, List
from schemas.shot import MediaBlock, Separator, StickerBlock, TextBlock, ShotGridBlock, Thumbnail

class DraftShotData(BaseModel):
    isDraft: bool
    authorId: str
    title: str
    rootBlock: MediaBlock
    blocks: List[Union[StickerBlock, Separator, TextBlock, ShotGridBlock, MediaBlock]]
    thumbnail: Optional[Thumbnail]
    createdAt: Union[int, float]

    class Config: 
        orm_mode = True

class DraftToPublish(DraftShotData):
    tags: List[str]
    enableMdSyntax: bool
    needFeedback: bool

    class Config: 
        orm_mode = True