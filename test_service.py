import pytest
import pytest_asyncio
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import clear_mappers

from service import Base, User, engine, async_session


@pytest.fixture(scope="module")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="module")
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session
        await session.rollback()
        await session.close()
        clear_mappers()


@pytest.mark.asyncio
async def test_add_and_get_user(db_session):
    await User.add(db_session, username='testuser1', name='John Doe')
    result = await User.get(db_session, username='testuser1')

    assert result.name == "John Doe"
    assert result.id != 2


@pytest.mark.asyncio
async def test_add_multiple_users(db_session):
    await User.add(db_session, username='testuser2', name='Jane Doe')
    result = await User.get(db_session, username='testuser2')

    assert result.name == "Jane Doe"
    assert result.id == 2


@pytest.mark.asyncio
@pytest.mark.xfail(raises=AssertionError)
async def test_wrong_user_name(db_session):
    await User.add(db_session, username='testuser3', name='John Doe')
    result = await User.get(db_session, username='testuser3')

    assert result.name == 'Jane Doe'


@pytest.mark.asyncio
@pytest.mark.xfail(raises=IntegrityError)
async def test_add_duplicate(db_session):
    await User.add(db_session, username="testuser1")
    await User.add(db_session, username="testuser1")
