import typing as t

from db_engine import get_session
from repositories import BaseRepository


class IUnitOfWork[Repository: BaseRepository](t.Protocol):
    async def __init__(self, repository: type[Repository]) -> None: ...

    
    async def __aenter__(self) -> None: ...


    async def __aexit__(self, *args) -> None: ...


    async def commit(self) -> None: ...


    async def rollback(self) -> None: ...


class UnitOfWork[Repository: BaseRepository]:
    def __init__(self, repository_type: type[Repository]) -> None:
        self.repository_type = repository_type
    

    async def __aenter__(self) -> t.Self:
        self.session = await get_session()
        self.repository = self.repository_type(self.session)
        # event.listen(self.engine, "before_cursor_execute", self.callback)

        return self


    async def __aexit__(self, *args) -> None:
        # event.remove(self.session.bind, "before_cursor_execute", self.callback)
        await self.rollback()
        await self.session.close()


    async def commit(self) -> None:
        await self.session.commit()


    async def rollback(self) -> None:
        await self.session.rollback()
