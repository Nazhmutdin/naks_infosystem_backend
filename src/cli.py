import pathlib
import json
import asyncio

import click
from naks_library.committer import SqlAlchemyCommitter

from app.application.dto import PersonalNaksCertificationDTO, PersonalDTO, AcstDTO, NdtDTO
from app.infrastructure.database.setup import create_engine, create_session_maker
from app.infrastructure.database.mappers import PersonalNaksCertificationMapper, PersonalMapper, AcstMapper, NdtMapper


@click.group()
def cli(): ...


engine = create_engine()
session_maker = create_session_maker(engine)


async def add_personal_naks_certifications(data: list[PersonalNaksCertificationDTO]):
    async with session_maker() as session:
        committer = SqlAlchemyCommitter(session)
        mapper = PersonalNaksCertificationMapper(session)

        for el in data:
            await mapper.insert(el)

        await committer.commit()


@cli.command("add-personal-naks-certifications")
@click.option("--src-path", "-sp", type=str)
def add_personal_naks_certifications_command(
    src_path: str,
):
    path = pathlib.Path(src_path)

    if not path.exists():
        raise ValueError(f"path ({src_path}) not exists")
    
    data = [PersonalNaksCertificationDTO(**el) for el in json.load(open(path, "r", encoding="utf-8"))]

    asyncio.run(add_personal_naks_certifications(data))


async def add_personals(data: list[PersonalDTO]):
    async with session_maker() as session:
        committer = SqlAlchemyCommitter(session)
        mapper = PersonalMapper(session)

        for el in data:
            await mapper.insert(el)

        await committer.commit()


@cli.command("add-personals")
@click.option("--src-path", "-sp", type=str)
def add_personals_command(
    src_path: str,
):
    path = pathlib.Path(src_path)

    if not path.exists():
        raise ValueError(f"path ({src_path}) not exists")
    
    data = [PersonalDTO(**el) for el in json.load(open(path, "r", encoding="utf-8"))]

    asyncio.run(add_personals(data))


async def add_ndts(data: list[NdtDTO]):
    async with session_maker() as session:
        committer = SqlAlchemyCommitter(session)
        mapper = NdtMapper(session)

        for el in data:
            await mapper.insert(el)

        await committer.commit()


@cli.command("add-ndts")
@click.option("--src-path", "-sp", type=str)
def add_ndts_command(
    src_path: str,
):
    path = pathlib.Path(src_path)

    if not path.exists():
        raise ValueError(f"path ({src_path}) not exists")
    
    data = [NdtDTO(**el) for el in json.load(open(path, "r", encoding="utf-8"))]

    asyncio.run(add_ndts(data))


async def add_acsts(data: list[AcstDTO]):
    async with session_maker() as session:
        committer = SqlAlchemyCommitter(session)
        mapper = AcstMapper(session)

        for el in data:
            await mapper.insert(el)

        await committer.commit()


@cli.command("add-acsts")
@click.option("--src-path", "-sp", type=str)
def add_acsts_command(
    src_path: str,
):
    path = pathlib.Path(src_path)

    if not path.exists():
        raise ValueError(f"path ({src_path}) not exists")
    
    data = [AcstDTO(**el) for el in json.load(open(path, "r", encoding="utf-8"))]

    asyncio.run(add_acsts(data))


if __name__ == "__main__":
    cli()
