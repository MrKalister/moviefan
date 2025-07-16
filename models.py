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


class BaseContent(BaseModel):
    title: str
    initial_title: str | None = None
    release_year: int | None = None
    # TODO: add func like lower() for content_type
    content_type: ContentType = ContentType.unknown


class Content(BaseContent):
    id: int
    created_user: User


class ContentCreate(BaseContent):
    created_user_id: int
