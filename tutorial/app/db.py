# What is ORM?
# ORM = Object Relational MapperIt's a tool that lets you interact with your database using Python objects instead of writing raw SQL.

from _collections_abc import AsyncGenerator
from unittest.mock import Base
import uuid
from xml.parsers.expat import model
# from sqlalchemy import create_engine, Column, String, Text, Integer, DateTime, Foreignkey
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID
from fastapi import Depends


DATABASE_URL="sqlite+aiosqlite:///./test.db"


# creating data model for storing the data in the database, for this we need to create a class which will inherit from the DeclarativeBase class of SQLAlchemy and then we need to define the table name and the columns of the table.


class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="posts")


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(DeclarativeBase.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


