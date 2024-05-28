from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import NullPool

from settings import Settings



DB_URL = "postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}".format(
    Settings.USER(), 
    Settings.DB_PASSWORD(), 
    Settings.HOST(), 
    Settings.PORT(), 
    Settings.DB_NAME()
)


engine = create_async_engine(DB_URL, poolclass = NullPool)


class Base(DeclarativeBase): ...


async def get_session() -> AsyncSession:

    session_maker = async_sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)

    return session_maker()
