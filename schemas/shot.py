from __future__ import annotations
from pydantic import BaseModel
from typing import Union, Optional

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
    ids: list[str]

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
    answers: list[CommentBlockNoAnswers]

    class Config: 
        orm_mode = True

class ShotDataForUpload(BaseModel):
    title: str
    rootBlock: ImageBlock
    blocks: Union[TextBlock, ShotGridBlock, ImageBlock]

    class Config: 
        orm_mode = True

class ShotData(BaseModel):
    isDraft: bool
    authorId: str
    title: str
    rootBlock: ImageBlock
    blocks: Union[TextBlock, ShotGridBlock, ImageBlock]
    createdAt: int
    likes: list[str]
    views: list[str]
    comments: list[CommentBlock]
    needFeedback: bool
    tags: list[str]
    thumbnail: Optional[ImageBlock]

    class Config: 
        orm_mode = True