from pydantic import BaseModel
from typing import Union, List

class NoteTextBlock(BaseModel):
    type: str
    text: str

    class Config: 
        orm_mode = True


class NoteHeadingBlock(BaseModel):
    type: str
    text: str

    class Config: 
        orm_mode = True

class ListItem(BaseModel):
    text: str

    class Config: 
        orm_mode = True

class NoteListBlock(BaseModel):
    type: str
    title: str
    list: List[ListItem]
    
    class Config: 
        orm_mode = True

class TaskListItem(BaseModel):
    checked: bool
    text: str

    class Config: 
        orm_mode = True

class NoteTaskListBlock(BaseModel):
    type: str
    title: str
    list: List[TaskListItem]
    
    class Config: 
        orm_mode = True

class Note(BaseModel):
    title: str
    isPinned: bool
    createdAt: Union[float, int]
    blocks: List[Union[NoteHeadingBlock, NoteTaskListBlock, NoteListBlock, NoteTextBlock]]
    authorId: str

    class Config: 
        orm_mode = True

class DocNote(BaseModel):
    doc_id: str
    title: str
    isPinned: bool
    createdAt: Union[float, int]
    blocks: List[Union[NoteHeadingBlock, NoteTaskListBlock, NoteListBlock, NoteTextBlock]]
    authorId: str

    class Config: 
        orm_mode = True