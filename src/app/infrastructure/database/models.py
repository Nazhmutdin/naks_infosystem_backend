from datetime import date
import uuid

from sqlalchemy.orm import Mapped, DeclarativeBase
from sqlalchemy.schema import UniqueConstraint, Index
import sqlalchemy as sa


__all__ = [
    "Base",
    "PersonalModel",
    "PersonalNaksCertificationModel",
    "NdtModel"
]


class Base(DeclarativeBase): ...


class PersonalModel(Base):
    __tablename__ = "personal_table"

    ident: Mapped[uuid.UUID] = sa.Column(sa.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    kleymo: Mapped[str | None] = sa.Column(sa.String(4), unique=True, nullable=True)
    name: Mapped[str] = sa.Column(sa.String(), nullable=False)
    birthday: Mapped[date | None] = sa.Column(sa.Date(), nullable=True)
    passport_number: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    exp_age: Mapped[int | None] = sa.Column(sa.Integer(), nullable=True)
    nation: Mapped[str | None] = sa.Column(sa.String(), nullable=True)

    __table_args__ = (
        Index("personal_ident_idx", ident),
        Index("personal_kleymo_idx", kleymo),
        Index("name_idx", name),
    )


class PersonalNaksCertificationModel(Base):
    __tablename__ = "personal_naks_certification_table"

    ident: Mapped[uuid.UUID] = sa.Column(sa.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    personal_ident: Mapped[uuid.UUID] = sa.Column(sa.UUID(as_uuid=True), sa.ForeignKey("personal_table.ident", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    certification_number: Mapped[str] = sa.Column(sa.String(), nullable=False)
    protocol_number: Mapped[str] = sa.Column(sa.String(), nullable=True)
    certification_date: Mapped[date] = sa.Column(sa.Date(), nullable=False)
    expiration_date: Mapped[date] = sa.Column(sa.Date(), nullable=False)
    expiration_date_fact: Mapped[date] = sa.Column(sa.Date(), nullable=False)
    insert: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    company: Mapped[str] = sa.Column(sa.String(), nullable=False)
    gtd: Mapped[list[str]] = sa.Column(sa.ARRAY(sa.String), nullable=False)
    method: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    detail_types: Mapped[list[str] | None] = sa.Column(sa.ARRAY(sa.String), nullable=True)
    joint_types: Mapped[list[str] | None] = sa.Column(sa.ARRAY(sa.String), nullable=True)
    materials: Mapped[list[str] | None] = sa.Column(sa.ARRAY(sa.String), nullable=True)
    detail_thikness_from: Mapped[float | None] = sa.Column(sa.Float(), nullable=True)
    detail_thikness_before: Mapped[float | None] = sa.Column(sa.Float(), nullable=True)
    outer_diameter_from: Mapped[float | None] = sa.Column(sa.Float(), nullable=True)
    outer_diameter_before: Mapped[float | None] = sa.Column(sa.Float(), nullable=True)
    rod_diameter_from: Mapped[float | None] = sa.Column(sa.Float(), nullable=True)
    rod_diameter_before: Mapped[float | None] = sa.Column(sa.Float(), nullable=True)
    detail_diameter_from: Mapped[float | None] = sa.Column(sa.Float(), nullable=True)
    detail_diameter_before: Mapped[float | None] = sa.Column(sa.Float(), nullable=True)
    html: Mapped[str] = sa.Column(sa.String(), nullable=False)


    __table_args__ = (
        UniqueConstraint(
            certification_number, 
            certification_date, 
            expiration_date_fact, 
            insert
        ),
        Index("personal_certification_ident_idx", ident),
        Index("certification_personal_ident_idx", personal_ident),
        Index("certification_idx", certification_number, certification_date, expiration_date_fact),
        Index("method_idx", method),
        Index("gtd_idx", gtd),
        Index("details_thikness_from_idx", detail_thikness_from),
        Index("details_thikness_before_idx", detail_thikness_before),
        Index("outer_diameter_from_idx", outer_diameter_from),
        Index("outer_diameter_before_idx", outer_diameter_before),
        Index("rod_diameter_from_idx", rod_diameter_from),
        Index("rod_diameter_before_idx", rod_diameter_before),
    )


class NdtModel(Base):
    __tablename__ = "ndt_table"
    
    ident: Mapped[uuid.UUID] = sa.Column(sa.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    personal_ident: Mapped[uuid.UUID] = sa.Column(sa.UUID(as_uuid=True), sa.ForeignKey("personal_table.ident", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    company: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    subcompany: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    project: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    welding_date: Mapped[date] = sa.Column(sa.Date(), nullable=False)
    ndt_type: Mapped[str] = sa.Column(sa.String(), nullable=False)
    total_welded: Mapped[float] = sa.Column(sa.Float(), nullable=False, default=0)
    total_ndt: Mapped[float] = sa.Column(sa.Float(), nullable=False, default=0)
    total_accepted: Mapped[float] = sa.Column(sa.Float(), nullable=False, default=0)
    total_rejected: Mapped[float] = sa.Column(sa.Float(), nullable=False, default=0)


    __table_args__ = (
        UniqueConstraint("personal_ident", "company", "subcompany", "project", "welding_date", "ndt_type"),
        Index("ndt_ident_idx", ident),
        Index("ndt_welding_date_idx", welding_date),
        Index("total_welded_idx", total_welded),
        Index("total_ndt_idx", total_ndt),
        Index("total_accepted_idx", total_accepted),
        Index("total_rejected_idx", total_rejected)
    )


class AcstModel(Base):
    __tablename__ = "acst_table"

    ident: Mapped[uuid.UUID] = sa.Column(sa.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    acst_number: Mapped[str] = sa.Column(sa.String(), nullable=False)
    certification_date: Mapped[date] = sa.Column(sa.Date(), nullable=False)
    expiration_date: Mapped[date] = sa.Column(sa.Date(), nullable=False)
    company: Mapped[str] = sa.Column(sa.String(), nullable=False)
    gtd: Mapped[list[str]] = sa.Column(sa.ARRAY(sa.String), nullable=False)
    method: Mapped[str | None] = sa.Column(sa.String(), nullable=True)
    detail_types: Mapped[list[str] | None] = sa.Column(sa.ARRAY(sa.String), nullable=True)
    joint_types: Mapped[list[str] | None] = sa.Column(sa.ARRAY(sa.String), nullable=True)
    materials: Mapped[list[str] | None] = sa.Column(sa.ARRAY(sa.String), nullable=True)
    thikness_from: Mapped[float | None] = sa.Column(sa.Float(), nullable=True)
    thikness_before: Mapped[float | None] = sa.Column(sa.Float(), nullable=True)
    diameter_from: Mapped[float | None] = sa.Column(sa.Float(), nullable=True)
    diameter_before: Mapped[float | None] = sa.Column(sa.Float(), nullable=True)
    preheating: Mapped[list[bool] | None] = sa.Column(sa.ARRAY(sa.BOOLEAN), nullable=True)
    heat_treatment: Mapped[list[bool] | None] = sa.Column(sa.ARRAY(sa.BOOLEAN), nullable=True)
    html: Mapped[str] = sa.Column(sa.String(), nullable=False)


    __table_args__ = (
        UniqueConstraint(
            acst_number
        ),
        Index("acst_ident_idx", ident),
        Index("acst_idx", acst_number, certification_date, expiration_date),
        Index("acst_method_idx", method),
        Index("acst_gtd_idx", gtd),
        Index("thikness_from_idx", thikness_from),
        Index("thikness_before_idx", thikness_before),
        Index("diameter_from_idx", diameter_from),
        Index("diameter_before_idx", diameter_before)
    )
