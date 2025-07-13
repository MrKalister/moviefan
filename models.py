from enum import Enum

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    age: int | None = None


class ContentType(str, Enum):
    movie = 'movie'
    serial = 'serial'
    unknown = 'unknown'


class Content(BaseModel):
    id: int
    title: str
    created_user: User
    initial_title: str | None = None
    release_year: int | None = None
    # TODO: add func like lower() for content_type
    content_type: ContentType = ContentType.unknown


class ContentCreate(BaseModel):
    title: str
    created_user_id: int
    initial_title: str | None = None
    release_year: int | None = None
    content_type: ContentType = ContentType.unknown
