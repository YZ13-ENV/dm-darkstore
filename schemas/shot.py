from __future__ import annotations
from pydantic import BaseModel
from typing import Union, Optional, List

class EmojiReaction(BaseModel):
    key: str
    emoji: str
    class Config: 
        orm_mode = True

class Reaction(BaseModel):
    reaction: EmojiReaction
    uid: str
    createdAt: Union[float, int]
    class Config: 
        orm_mode = True

class Thumbnail(BaseModel):
    width: int
    height: int
    link: str

# blocks
class MediaBlock(BaseModel):
    type: str
    link: str

    class Config: 
        orm_mode = True

class Separator(BaseModel):
    type: str
    withIcon: bool
    uid: str

    class Config: 
        orm_mode = True

class StickerBlock(BaseModel):
    type: str
    x: int
    y: int
    width: Optional[int]
    height: Optional[int]
    rotate: int
    code: str

    class Config: 
        orm_mode = True

class TextBlock(BaseModel):
    type: str
    size: Optional[int]
    align: Optional[str]
    isBold: Optional[bool]
    isItalic: Optional[bool]
    text: str

    class Config: 
        orm_mode = True

class ShotGridBlock(BaseModel):
    type: str
    title: str
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
    id: str
    authorId: str
    text: str
    createdAt: Union[int, float]
    answers: List[Union[None, CommentBlockNoAnswers]]
    reactions: List[Reaction]

    class Config: 
        orm_mode = True

class NewCommentBlock(BaseModel):
    authorId: str
    text: str
    createdAt: Union[int, float]
    answers: List[Union[None, CommentBlockNoAnswers]]
    reactions: List[Reaction]

    class Config: 
        orm_mode = True    

class ShotDataForUpload(BaseModel):
    title: str
    rootBlock: MediaBlock
    blocks: List[Union[StickerBlock, Separator, TextBlock, ShotGridBlock, MediaBlock]]
    thumbnail: Optional[Thumbnail]

    class Config: 
        orm_mode = True


class ThumbnailThree(BaseModel):
    desktop: Thumbnail
    mobile: Thumbnail
    thumbnail: Thumbnail

    class Config: 
        orm_mode = True

class ViewWithTimestamp(BaseModel):
    uid: str
    createdAt: Union[float, int]
    class Config: 
        orm_mode = True

class LikeWithTimestamp(BaseModel):
    uid: str
    createdAt: Union[float, int]
    class Config: 
        orm_mode = True


class ShotData(BaseModel):
    isDraft: bool
    authorId: str
    title: str
    rootBlock: MediaBlock
    blocks: List[Union[StickerBlock, Separator, TextBlock, ShotGridBlock, MediaBlock]]
    createdAt: Union[int, float]
    likes: List[Union[str, LikeWithTimestamp]]
    views: List[Union[str, LikeWithTimestamp]]
    comments: List[CommentBlock]
    needFeedback: bool
    tags: List[str]
    thumbnail: Optional[Thumbnail]

    class Config: 
        orm_mode = True

class DocShotData(BaseModel):
    doc_id: str
    isDraft: bool
    authorId: str
    title: str
    rootBlock: MediaBlock
    blocks: List[Union[StickerBlock, Separator, TextBlock, ShotGridBlock, MediaBlock]]
    createdAt: Union[int, float]
    likes: List[str]
    views: List[str]
    comments: List[CommentBlock]
    needFeedback: bool
    tags: List[str]
    thumbnail: Optional[Thumbnail]

    class Config: 
        orm_mode = True
