from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session


class UserDTO(BaseModel):
    id: int
    username: str


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    name = Column(String(40), nullable=True)

    @classmethod
    async def add(cls, db: AsyncSession, **kwargs):
        await db.execute(insert(cls).values(**kwargs))
        await db.commit()

    @classmethod
    async def get(cls, db: AsyncSession, username: str) -> UserDTO:
        result = await db.execute(select(cls).filter_by(username=username))
        return result.scalars().first()

