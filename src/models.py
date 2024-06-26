from datetime import datetime, date
import typing as t
import uuid

from sqlalchemy.orm import Mapped, DeclarativeBase, attributes, relationship
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.schema import UniqueConstraint, Index
import sqlalchemy as sa
from naks_library import is_uuid


__all__ = [
    "Base",
    "WelderModel",
    "WelderCertificationModel",
    "NDTModel"
]

class Base(DeclarativeBase): 

    @classmethod
    async def get(cls, conn: AsyncConnection, ident: uuid.UUID | str):
        stmt = cls._dump_get_stmt(ident)
        response = await conn.execute(stmt)
        result = response.mappings().one_or_none()

        return result
        

    @classmethod
    async def get_many(cls, conn: AsyncConnection, expression: sa.ColumnElement, limit: int, offset: int):
        stmt = cls._dump_get_many_stmt(expression)

        amount = await cls.count(conn, stmt)

        if limit:
            stmt = stmt.limit(limit)

        if offset:
            stmt = stmt.offset(offset)
        
        response = await conn.execute(stmt)

        result = response.mappings().all()
        
        return (result, amount)
        

    @classmethod
    async def create(cls, data: list[dict], conn: AsyncConnection):
        stmt = cls._dump_create_stmt(
            data
        )

        await conn.execute(stmt)


    @classmethod
    async def update(cls, conn: AsyncConnection, ident: uuid.UUID | str, data: dict[str, t.Any]):
        stmt = cls._dump_update_stmt(ident, data)
        await conn.execute(stmt)


    @classmethod
    async def delete(cls, conn: AsyncConnection, ident: uuid.UUID | str):
        stmt = cls._dump_delete_stmt(ident)
        await conn.execute(stmt)


    @classmethod
    async def count(cls, conn: AsyncConnection, stmt: sa.Select | None = None):
        if isinstance(stmt, sa.ColumnElement):
            stmt.select(sa.func.count())

            return (await conn.execute(stmt)).scalar_one()

        else:
            return (await conn.execute(sa.select(sa.func.count()).select_from(cls).distinct())).scalar_one()


    @classmethod
    def _get_column(cls, ident: str | uuid.UUID):
        return sa.inspect(cls).primary_key[0]


    @classmethod
    def _dump_create_stmt(cls, data: list[dict[str, t.Any]]):
        return sa.insert(cls).values(
            data
        )


    @classmethod
    def _dump_get_stmt(cls, ident: str | uuid.UUID):
        return sa.select(cls).where(
            cls._get_column(ident) == ident
        )


    @classmethod
    def _dump_get_many_stmt(cls, expression: sa.ColumnExpressionArgument):
        return sa.select(cls).filter(expression)
    

    @classmethod
    def _dump_update_stmt(cls, ident: str | uuid.UUID, data: dict[str, t.Any]):
        return sa.update(cls).where(
            cls._get_column(ident) == ident
        ).values(
            **data
        )


    @classmethod
    def _dump_delete_stmt(cls, ident: str | uuid.UUID):
        return sa.delete(cls).where(
            cls._get_column(ident) == ident
        )


class WelderModel(Base):
    __tablename__ = "welder_table"

    ident: Mapped[uuid.UUID] = sa.Column(sa.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    kleymo: Mapped[str] = sa.Column(sa.String(4), unique=True)
    name: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    birthday: Mapped[str | None] = sa.Column(sa.Date(), nullable=True)
    sicil: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    passport_number: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    nation: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    status: Mapped[str] = sa.Column(sa.SMALLINT, default=0)
    certifications: Mapped[list["WelderCertificationModel"]] = relationship("WelderCertificationModel", back_populates="welder")
    ndts: Mapped[list["NDTModel"]] = relationship("NDTModel", back_populates="welder")

    __table_args__ = (
        Index("welder_ident_idx", ident),
        Index("welder_kleymo_idx", kleymo),
        Index("name_idx", name),
    )


    @classmethod
    def _dump_get_many_stmt(cls, expression: sa.ColumnExpressionArgument):
        return sa.select(cls).join(
            WelderCertificationModel
        ).filter(expression).distinct()


    @classmethod
    def _get_column(cls, ident: str | uuid.UUID) -> attributes.InstrumentedAttribute:
        if is_uuid(ident):
            return WelderModel.ident
        
        return WelderModel.kleymo


class WelderCertificationModel(Base):
    __tablename__ = "welder_certification_table"

    ident: Mapped[uuid.UUID] = sa.Column(sa.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    kleymo: Mapped[str] = sa.Column(sa.String(4), sa.ForeignKey("welder_table.kleymo", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    job_title: Mapped[str] = sa.Column(sa.String(), nullable=True)
    certification_number: Mapped[str] = sa.Column(sa.String(), nullable=False)
    certification_date: Mapped[date] = sa.Column(sa.Date(), nullable=False)
    expiration_date: Mapped[date] = sa.Column(sa.Date(), nullable=False)
    expiration_date_fact: Mapped[date] = sa.Column(sa.Date(), nullable=False)
    insert: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    certification_type: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    company: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    gtd: Mapped[list[str] | None] = sa.Column(sa.ARRAY(sa.String), nullable=True)
    method: Mapped[str] = sa.Column(sa.String(), nullable=True)
    details_type: Mapped[list[str] | None] = sa.Column(sa.ARRAY(sa.String), nullable=True)
    joint_type: Mapped[list[str] | None] = sa.Column(sa.ARRAY(sa.String), nullable=True)
    welding_materials_groups: Mapped[list[str] | None] = sa.Column(sa.ARRAY(sa.String), nullable=True)
    welding_materials: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    details_thikness_from: Mapped[float | None] = sa.Column(sa.Float(), nullable=True)
    details_thikness_before: Mapped[float | None] = sa.Column(sa.Float(), nullable=True)
    outer_diameter_from: Mapped[float | None] = sa.Column(sa.Float(), nullable=True)
    outer_diameter_before: Mapped[float | None] = sa.Column(sa.Float(), nullable=True)
    welding_position: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    connection_type: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    rod_diameter_from: Mapped[float | None] = sa.Column(sa.Float(), nullable=True)
    rod_diameter_before: Mapped[float | None] = sa.Column(sa.Float(), nullable=True)
    rod_axis_position: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    weld_type: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    joint_layer: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    sdr: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    automation_level: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    details_diameter_from: Mapped[float | None] = sa.Column(sa.Float(), nullable=True)
    details_diameter_before: Mapped[float | None] = sa.Column(sa.Float(), nullable=True)
    welding_equipment: Mapped[str | None] = sa.Column(sa.String(), nullable=True)

    welder: Mapped[WelderModel] = relationship("WelderModel", back_populates="certifications")

    __table_args__ = (
        UniqueConstraint(
            "kleymo", 
            "certification_number", 
            "certification_date", 
            "expiration_date_fact", 
            "insert"
        ),
        Index("welder_certification_ident_idx", ident),
        Index("welder_certification_kleymo_idx", kleymo),
        Index("certification_idx", certification_number, certification_date, expiration_date_fact),
        Index("method_idx", method),
        Index("gtd_idx", gtd),
        Index("details_thikness_from_idx", details_thikness_from),
        Index("details_thikness_before_idx", details_thikness_before),
        Index("outer_diameter_from_idx", outer_diameter_from),
        Index("outer_diameter_before_idx", outer_diameter_before),
        Index("rod_diameter_from_idx", rod_diameter_from),
        Index("rod_diameter_before_idx", rod_diameter_before),
    )
  

class NDTModel(Base):
    __tablename__ = "ndt_table"
    
    ident: Mapped[uuid.UUID] = sa.Column(sa.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    kleymo: Mapped[str] = sa.Column(sa.String(4), sa.ForeignKey("welder_table.kleymo", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    company: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    subcompany: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    project: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    welding_date: Mapped[date] = sa.Column(sa.Date(), nullable=False)
    ndt_type: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    total_welded: Mapped[float | None] = sa.Column(sa.Float(), nullable=False, default=0)
    total_ndt: Mapped[float | None] = sa.Column(sa.Float(), nullable=False, default=0)
    accepted: Mapped[float | None] = sa.Column(sa.Float(), nullable=False, default=0)
    rejected: Mapped[float | None] = sa.Column(sa.Float(), nullable=False, default=0)
    
    welder: Mapped[WelderModel] = relationship("WelderModel", back_populates="ndts")


    __table_args__ = (
        UniqueConstraint("kleymo", "company", "subcompany", "project", "welding_date", "ndt_type"),
        Index("ndt_ident_idx", ident),
        Index("ndt_idx", kleymo, company, subcompany, project),
        Index("total_welded_idx", total_welded),
        Index("total_ndt_idx", total_ndt),
        Index("accepted_idx", accepted),
        Index("rejected_idx", rejected)
    )
