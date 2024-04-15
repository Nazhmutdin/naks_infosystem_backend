from asyncio import run
from time import sleep

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import NullPool

from settings import Settings

from async_lru import alru_cache


DB_URL = "postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}".format(
    Settings.USER(), 
    Settings.DB_PASSWORD(), 
    Settings.HOST(), 
    Settings.PORT(), 
    Settings.DB_NAME()
)

print(DB_URL)


engine = create_async_engine(DB_URL, poolclass=NullPool)


class Base(DeclarativeBase): ...


async def get_session() -> AsyncSession:
    session_maker = await get_session_maker()

    return session_maker()


@alru_cache()
async def get_session_maker():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
