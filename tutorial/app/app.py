from fastapi import FastAPI, HTTPException
from streamlit import title
from app.schemas import PostCreate
from app.db import create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield




app= FastAPI(lifespan=lifespan)
text_posts = {
    1: {"title": "First Post", "content": "This is the first post."},
    2: {"title": "Second Post", "content": "This is the second post."},
    3: {"title": "Third Post", "content": "This is the third post."},
    4: {"title": "Fourth Post", "content": "This is the fourth post."},
    5: {"title": "Fifth Post", "content": "This is the fifth post."},
    6: {"title": "Sixth Post", "content": "This is the sixth post."},
    7: {"title": "Seventh Post", "content": "This is the seventh post."},
    8: {"title": "Eighth Post", "content": "This is the eighth post."},
    9: {"title": "Ninth Post", "content": "This is the ninth post."},
    10: {"title": "Tenth Post", "content": "This is the tenth post."}
}
@app.get("/posts")
# using query paramter, example using limit as quesy paramter which limit the number of object to be recived from the number of post
def get_all_posts(limit: int =  None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts


@app.get("/posts/{post_id}")    #post_id is called path parameter
def get_post(post_id: int): 
    if post_id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts[post_id]


# posting a post , for this u need the request body which should be mentioned in schemas file.

@app.post("/post")
def create_post(post : PostCreate) -> PostCreate:  # basically when a request comes from client the req. body is checked ny fastapi whether it matches with the schema of PostCraete class of not 
    new_post = {"title":post.title,"content":post.content}
    text_posts[max(text_posts.keys())+1] = new_post
    return {"message": "Post created successfully", "post": new_post}

# validating the data output type that is what type of data it returns on any request made for this endpoint, that is acheived by def create_post(post : PostCreate) -> PostCreate: the PostCraete after the arrow "->" signifies that the return type of the function is PostCreate class
