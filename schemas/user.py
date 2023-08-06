from pydantic import BaseModel


class UserShortData(BaseModel):
    email: str
    displayName: str
    photoUrl: str

    class Config: 
        orm_mode = True