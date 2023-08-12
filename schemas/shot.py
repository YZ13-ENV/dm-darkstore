from __future__ import annotations
from pydantic import BaseModel
from typing import Union, Optional, List

class Thumbnail(BaseModel):
    width: int
    height: int
    link: str

class MediaBlock(BaseModel):
    type: str
    link: str

    class Config: 
        orm_mode = True

class TextBlock(BaseModel):
    type: str
    size: int
    align: str
    isBold: bool
    isItalic: bool
    text: str

    class Config: 
        orm_mode = True

class ShotGridBlock(BaseModel):
    type: str
    ids: List[str]

    class Config: 
        orm_mode = True

class CommentBlockNoAnswers(BaseModel):
    authorId: str
    text: str
    createdAt: Union[int, float]

    class Config: 
        orm_mode = True

class CommentBlock(BaseModel):
    authorId: str
    text: str
    createdAt: Union[int, float]
    answers: List[CommentBlockNoAnswers]

    class Config: 
        orm_mode = True

class ShotDataForUpload(BaseModel):
    title: str
    rootBlock: MediaBlock
    blocks: List[Union[TextBlock, ShotGridBlock, MediaBlock]]

    class Config: 
        orm_mode = True

class ThumbnailThree(BaseModel):
    desktop: Thumbnail
    mobile: Thumbnail
    thumbnail: Thumbnail

class ShotData(BaseModel):
    isDraft: bool
    authorId: str
    title: str
    rootBlock: MediaBlock
    blocks: List[Union[TextBlock, ShotGridBlock, MediaBlock]]
    createdAt: Union[int, float]
    likes: List[str]
    views: List[str]
    comments: List[CommentBlock]
    needFeedback: bool
    tags: List[str]
    thumbnail: Optional[Thumbnail]

    class Config: 
        orm_mode = True