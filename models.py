from typing import Union

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    age: Union[int, None] = None


class Content(BaseModel):
    id: int
    title: str
    created_user: User
    initial_title: Union[str, None] = None
    release_year: Union[int, None] = None


class ContentCreate(BaseModel):
    title: str
    created_user_id: int
    initial_title: Union[str, None] = None
    release_year: Union[int, None] = None
