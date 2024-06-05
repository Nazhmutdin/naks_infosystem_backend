import typing as t

from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWorkUpdated:

    async def __aenter__(self, session: AsyncSession) -> t.Self:
        self.session = session
        return self


    async def __aexit__(self, *args) -> None:
        await self.rollback()
        await self.session.close()


    async def commit(self) -> None:
        await self.session.commit()


    async def rollback(self) -> None:
        await self.session.rollback()
