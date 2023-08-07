from __future__ import annotations
from pydantic import BaseModel
from typing import Union, Optional, List

class ImageBlock(BaseModel):
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
    createdAt: int

    class Config: 
        orm_mode = True

class CommentBlock(BaseModel):
    authorId: str
    text: str
    createdAt: int
    answers: List[CommentBlockNoAnswers]

    class Config: 
        orm_mode = True

class ShotDataForUpload(BaseModel):
    title: str
    rootBlock: ImageBlock
    blocks: List[Union[TextBlock, ShotGridBlock, ImageBlock]]

    class Config: 
        orm_mode = True

class ShotData(BaseModel):
    isDraft: bool
    authorId: str
    title: str
    rootBlock: ImageBlock
    blocks: List[Union[TextBlock, ShotGridBlock, ImageBlock]]
    createdAt: int
    likes: List[str]
    views: List[str]
    comments: List[CommentBlock]
    needFeedback: bool
    tags: List[str]
    thumbnail: Optional[ImageBlock]

    class Config: 
        orm_mode = True