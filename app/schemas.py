from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str
    owner: UserOut
    # published: bool = True

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id : int


    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str]


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True
