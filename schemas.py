from typing import Optional
from pydantic import BaseModel

class UserShortData(BaseModel):
    email: str
    displayName: str
    photoUrl: str

    class Config: 
        orm_mode = True


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
    blocks: list[TextBlock | ShotGridBlock | ImageBlock]

    class Config: 
        orm_mode = True

class DraftShotData(BaseModel):
    isDraft: bool
    authorId: str
    title: str
    rootBlock: ImageBlock
    blocks: list[TextBlock | ShotGridBlock | ImageBlock]
    createdAt: int

    class Config: 
        orm_mode = True

class ShotData(BaseModel):
    isDraft: bool
    authorId: str
    title: str
    rootBlock: ImageBlock
    blocks: list[TextBlock | ShotGridBlock | ImageBlock]
    createdAt: int
    likes: list[str]
    views: list[str]
    comments: list[CommentBlock]
    needFeedback: bool
    tags: list[str]
    thumbnail: Optional[ImageBlock]

    class Config: 
        orm_mode = True