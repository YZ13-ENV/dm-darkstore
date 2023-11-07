from pydantic import BaseModel


class UserShortData(BaseModel):
    email: str
    displayName: str
    photoUrl: str
    isSubscriber: bool

    class Config: 
        orm_mode = True