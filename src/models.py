from datetime import date
import uuid

from sqlalchemy.orm import Mapped, attributes, DeclarativeBase
from sqlalchemy.schema import UniqueConstraint, Index
import sqlalchemy as sa
from naks_library import is_uuid, CRUDMixin


__all__ = [
    "Base",
    "PersonalModel",
    "PersonalCertificationModel",
    "NDTModel"
]


class Base(DeclarativeBase, CRUDMixin): ...


class PersonalModel(Base):
    __tablename__ = "personal_table"

    ident: Mapped[uuid.UUID] = sa.Column(sa.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    kleymo: Mapped[str | None] = sa.Column(sa.String(4), unique=True, nullable=True)
    name: Mapped[str] = sa.Column(sa.String())
    birthday: Mapped[str | None] = sa.Column(sa.Date(), nullable=True)
    sicil: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    passport_number: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    nation: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    status: Mapped[str] = sa.Column(sa.SMALLINT, default=0)

    __table_args__ = (
        Index("personal_ident_idx", ident),
        Index("personal_kleymo_idx", kleymo),
        Index("name_idx", name),
    )


    @classmethod
    def _dump_get_many_stmt(cls, expression: sa.ColumnExpressionArgument):
        return sa.select(cls).join(
            PersonalCertificationModel
        ).filter(expression).distinct()


    @classmethod
    def _get_column(cls, ident: str | uuid.UUID) -> attributes.InstrumentedAttribute:
        if is_uuid(ident):
            return PersonalModel.ident
        
        return PersonalModel.kleymo


class PersonalCertificationModel(Base):
    __tablename__ = "personal_certification_table"

    ident: Mapped[uuid.UUID] = sa.Column(sa.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    kleymo: Mapped[str] = sa.Column(sa.String(4), sa.ForeignKey("personal_table.kleymo", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
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


    __table_args__ = (
        UniqueConstraint(
            "kleymo", 
            "certification_number", 
            "certification_date", 
            "expiration_date_fact", 
            "insert"
        ),
        Index("personal_certification_ident_idx", ident),
        Index("personal_certification_kleymo_idx", kleymo),
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
    kleymo: Mapped[str] = sa.Column(sa.String(4), sa.ForeignKey("personal_table.kleymo", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    company: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    subcompany: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    project: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    welding_date: Mapped[date] = sa.Column(sa.Date(), nullable=False)
    ndt_type: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    total_welded: Mapped[float | None] = sa.Column(sa.Float(), nullable=False, default=0)
    total_ndt: Mapped[float | None] = sa.Column(sa.Float(), nullable=False, default=0)
    accepted: Mapped[float | None] = sa.Column(sa.Float(), nullable=False, default=0)
    rejected: Mapped[float | None] = sa.Column(sa.Float(), nullable=False, default=0)


    __table_args__ = (
        UniqueConstraint("kleymo", "company", "subcompany", "project", "welding_date", "ndt_type"),
        Index("ndt_ident_idx", ident),
        Index("ndt_idx", kleymo, company, subcompany, project),
        Index("total_welded_idx", total_welded),
        Index("total_ndt_idx", total_ndt),
        Index("accepted_idx", accepted),
        Index("rejected_idx", rejected)
    )
