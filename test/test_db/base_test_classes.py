from datetime import date
import pytest
from repositories import BaseRepository
from services.db_services import BaseDBService
from utils.uow import UnitOfWork
from utils.funcs import str_to_datetime
from errors import CreateDBException
from shemas import *



class BaseTestRepository[Shema: BaseShema]:
    __create_shema__: type[BaseShema]
    __update_shema__: type[BaseShema]
    __repository__: type[BaseRepository]


    async def test_add(self, data: list[Shema]) -> None:
        async with UnitOfWork(repository_type=self.__repository__) as uow:
            for el in data:
                await uow.repository.add(self.__create_shema__.model_validate(el, from_attributes=True))
                assert await uow.repository.get(el.ident) == el

            assert await uow.repository.count() == len(data)

            await uow.commit()

    
    async def test_get(self, attr: str, el: Shema) -> None:
        async with UnitOfWork(repository_type=self.__repository__) as uow:

            assert await uow.repository.get(getattr(el, attr)) == el


    async def test_res_type(self, ident: int | str, expectation: type[Shema]) -> None:
        async with UnitOfWork(repository_type=self.__repository__) as uow:
            assert type(await uow.repository.get(ident)) == expectation


    async def test_add_existing(self, data: Shema) -> None:
        async with UnitOfWork(repository_type=self.__repository__) as uow:
            with pytest.raises(CreateDBException):
                await uow.repository.add(self.__create_shema__.model_validate(data, from_attributes=True))


    async def test_update(self, ident: str, data: dict) -> None:
        async with UnitOfWork(repository_type=self.__repository__) as uow:

            await uow.repository.update(ident, self.__update_shema__.model_validate(data, from_attributes=True))
            el = await uow.repository.get(ident)

            for key, value in data.items():
                if isinstance(getattr(el, key), date):
                    assert getattr(el, key) == str_to_datetime(value, False).date()
                    continue

                assert getattr(el, key) == value

            await uow.commit()

    
    async def test_delete(self, item: Shema) -> None:
        async with UnitOfWork(repository_type=self.__repository__) as uow:

            await uow.repository.delete(item.ident)

            assert not bool(await uow.repository.get(item.ident))

            await uow.repository.add(self.__create_shema__.model_validate(item, from_attributes=True))
            await uow.commit()



class BaseTestDBService[Shema: BaseShema]:
    service: BaseDBService

    async def test_add(self, item: Shema) -> None:
        await self.service.add(**item.model_dump())
        assert await self.service.get(item.ident) == item


    async def test_add_many(self, items: list[Shema]) -> None:
        data = [item.model_dump() for item in items]

        await self.service.add_many(data)


    async def test_get(self, attr: str, item: Shema) -> None:

        assert await self.service.get(getattr(item, attr)) == item


    async def test_update(self, ident: str, data: dict) -> None:

        assert await self.service.get(ident)

        await self.service.update(ident, **data)
        item = await self.service.get(ident)

        for key, value in data.items():
            if isinstance(getattr(item, key), date):
                assert getattr(item, key) == str_to_datetime(value, False).date()
                continue

            assert getattr(item, key) == value

    
    async def test_fail_update(self, ident: str, data: dict, exception) -> None:
        with pytest.raises(exception):
            await self.service.update(ident, **data)


    async def test_delete(self, item: Shema) -> None:

        await self.service.delete(item.ident)

        assert not bool(await self.service.get(item.ident))

        await self.service.add(**item.model_dump())
