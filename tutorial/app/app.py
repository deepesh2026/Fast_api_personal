from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Form
from streamlit import title
from app.schemas import PostCreate
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import tempfile
import shutil
import os



@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app= FastAPI(lifespan=lifespan)

@app.post("/upload")
async def upload_post(
    
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session)
):
    #create a copy of the uploaded file and save it to a temporary location
    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        upload_result = imagekit.upload_file(
            file=open(temp_file_path, "rb"),
            file_name=file.filename,
            options=UploadFileRequestOptions(use_unique_file_name=True,tags=["backend-upload"])
        )
        if upload_result.response.http_status_code == 200:
            post = Post(caption=caption,url=upload_result.url,file_type="video" if file.content_type.startswith("video/") else "photo", file_name=upload_result.name)
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post
           
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
    


@app.get("/feed")
async def get_feed(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    posts_data = []
    for post in posts:
        posts_data.append({
            "id": str(post.id),
            "caption": post.caption,
            "url": post.url,
            "file_type": post.file_type,
            "file_name": post.file_name,
            "created_at": post.created_at.isoformat(),
        })
        # posts_data.append(post_data)
    return {"posts": posts_data}