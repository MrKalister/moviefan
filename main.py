import logging
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse

from models import ContentCreate, Content, User

log = logging.getLogger(__name__)

app = FastAPI(
    title='Movie Fan',
    summary='I can remember your list to watch. Look at this and get know how',
    default_response_class=ORJSONResponse,
)

users = [
    {'id': 1, 'name': 'Alex', 'age': 20},
    {'id': 2, 'name': 'Bob', 'age': 25},
    {'id': 3, 'name': 'Max', 'age': 30},
]
user_objs = [User(**user) for user in users]
content_id = 0
contents_objs = []


# Endpoints
@app.post('/contents')
async def add_content(content_create: ContentCreate) -> Content:
    global content_id
    created_user = next((user for user in user_objs if user.id == content_create.created_user_id))
    content_id += 1
    try:
        content = Content(
            id=content_id,
            title=content_create.title,
            created_user=created_user,
            initial_title=content_create.initial_title,
            release_year=content_create.release_year
        )
    except Exception as e:
        log.error(f'An error occurred while creating content: {e}')
        raise HTTPException(status_code=404, detail='An error occurred while creating content')
    contents_objs.append(content)

    return content


@app.get('/content/{id}')
async def get_content(id: int) -> Content:
    for content in contents_objs:
        if content.id == id:
            return content

    log.error('Content was not been found')
    raise HTTPException(status_code=404, detail='Content was not been found')


@app.get('/contents')
async def get_contents() -> List[Content]:
    return contents_objs


@app.get('/users')
async def get_users() -> List[User]:
    return user_objs
