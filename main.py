import logging
from typing import List, Annotated

from fastapi import FastAPI, HTTPException, Query
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
content_id = 1
contents_objs = []


# Endpoints
@app.post('/contents')
async def create_content(content_data: ContentCreate) -> Content:
    global content_id

    # Find user
    created_user = next((u for u in user_objs if u.id == content_data.created_user_id), None)
    if not created_user:
        raise HTTPException(404, "User not found")

    # Check for duplicate content
    if any(
            c.release_year == content_data.release_year and
            c.title == content_data.title and
            c.created_user.id == content_data.created_user_id
            for c in contents_objs
    ):
        raise HTTPException(409, "Content already exists")

    # Create and add new content
    content = Content(
        id=content_id,
        **content_data.model_dump(exclude={'created_user_id'}),
        created_user=created_user
    )
    content_id += 1
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
