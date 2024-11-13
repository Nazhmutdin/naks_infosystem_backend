import pathlib
import json
import asyncio

import click
from naks_library.commiter import SqlAlchemyCommitter

from app.application.dto import PersonalNaksCertificationDTO, PersonalDTO
from app.infrastructure.database.setup import create_engine, create_session_maker
from app.infrastructure.database.mappers import PersonalNaksCertificationMapper, PersonalMapper


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
            print(el)

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


if __name__ == "__main__":
    cli()
