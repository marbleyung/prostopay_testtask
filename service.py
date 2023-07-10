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
    '''
    using Base(DeclarativeBase) instead of deprecated Base = declarative_base()
    '''
    pass


async def init_models():
    '''
    create and recreate database since it is test option, not a production
    in production it is highly recommend to use migration system instead
    :return:
    '''
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session


class UserDTO(BaseModel):
    '''
    simple user schema with optional `name` field
    '''
    id: int
    username: str
    name: str | None


class User(Base):
    '''
    since the task is to create a simple User model with 'get' and 'post' (add) methods
    it is no need to create a lot of complicated fields
    '''
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    name = Column(String(40), nullable=True)

    '''
    both method are class methods to be able to get AsyncSesssion from outer scope 
    '''
    @classmethod
    async def add(cls, db: AsyncSession, **kwargs):
        '''
        insert to class-named table unzipped dict of kwargs
        :param db:
        :param kwargs:
        :return:
        '''
        await db.execute(insert(cls).values(**kwargs))
        await db.commit()

    @classmethod
    async def get(cls, db: AsyncSession, username: str) -> UserDTO:
        result = await db.execute(select(cls).filter_by(username=username))
        return result.scalars().first()

