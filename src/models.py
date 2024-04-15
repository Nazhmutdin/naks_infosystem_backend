from datetime import datetime, date
import uuid

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import String, Column, Date, ForeignKey, Float, ARRAY, Boolean, DateTime, SMALLINT, UUID, Enum

from db_engine import Base


# class UserModel(Base):
#     __tablename__ = "user_table"

#     ident: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
#     name: Mapped[str] = Column(String(), nullable=False)
#     login: Mapped[str] = Column(String(), unique=True, nullable=False)
#     hashed_password: Mapped[str] = Column(String(), nullable=False)
#     email: Mapped[str | None] = Column(String(), nullable=True)
#     sign_date: Mapped[datetime] = Column(DateTime(), nullable=False)
#     update_date: Mapped[datetime] = Column(DateTime(), nullable=False)
#     login_date: Mapped[datetime] = Column(DateTime(), nullable=False)
#     is_superuser: Mapped[bool] = Column(Boolean(), nullable=False)


class WelderModel(Base):
    __tablename__ = "welder_table"

    ident: Mapped[uuid.UUID] = Column(UUID(), primary_key=True, nullable=False, default=uuid.uuid4)
    kleymo: Mapped[str] = Column(String(4), unique=True)
    name: Mapped[str | None] = Column(String(), nullable=True)
    birthday: Mapped[str | None] = Column(Date(), nullable=True)
    sicil: Mapped[str | None] = Column(String(), nullable=True)
    passport_number: Mapped[str | None] = Column(String(), nullable=True)
    nation: Mapped[str | None] = Column(String(), nullable=True)
    status: Mapped[str] = Column(SMALLINT, default=0)
    certifications: Mapped[list["WelderCertificationModel"]] = relationship("WelderCertificationModel", back_populates="welder")
    ndts: Mapped[list["NDTModel"]] = relationship("NDTModel", back_populates="welder")


class WelderCertificationModel(Base):
    __tablename__ = "welder_certification_table"

    ident: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    kleymo: Mapped[str] = Column(String(4), ForeignKey("welder_table.kleymo", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    job_title: Mapped[str] = Column(String(), nullable=True)
    certification_number: Mapped[str] = Column(String(), nullable=False)
    certification_date: Mapped[date] = Column(Date(), nullable=False)
    expiration_date: Mapped[date] = Column(Date(), nullable=False)
    expiration_date_fact: Mapped[date] = Column(Date(), nullable=False)
    insert: Mapped[str | None] = Column(String(), nullable=True)
    certification_type: Mapped[str | None] = Column(String(), nullable=True)
    company: Mapped[str | None] = Column(String(), nullable=True)
    gtd: Mapped[list[str] | None] = Column(ARRAY(String), nullable=True)
    method: Mapped[str] = Column(String(), nullable=True)
    details_type: Mapped[list[str] | None] = Column(ARRAY(String), nullable=True)
    joint_type: Mapped[list[str] | None] = Column(ARRAY(String), nullable=True)
    welding_materials_groups: Mapped[list[str] | None] = Column(ARRAY(String), nullable=True)
    welding_materials: Mapped[str | None] = Column(String(), nullable=True)
    details_thikness_from: Mapped[float | None] = Column(Float(), nullable=True)
    details_thikness_before: Mapped[float | None] = Column(Float(), nullable=True)
    outer_diameter_from: Mapped[float | None] = Column(Float(), nullable=True)
    outer_diameter_before: Mapped[float | None] = Column(Float(), nullable=True)
    welding_position: Mapped[str | None] = Column(String(), nullable=True)
    connection_type: Mapped[str | None] = Column(String(), nullable=True)
    rod_diameter_from: Mapped[float | None] = Column(Float(), nullable=True)
    rod_diameter_before: Mapped[float | None] = Column(Float(), nullable=True)
    rod_axis_position: Mapped[str | None] = Column(String(), nullable=True)
    weld_type: Mapped[str | None] = Column(String(), nullable=True)
    joint_layer: Mapped[str | None] = Column(String(), nullable=True)
    sdr: Mapped[str | None] = Column(String(), nullable=True)
    automation_level: Mapped[str | None] = Column(String(), nullable=True)
    details_diameter_from: Mapped[float | None] = Column(Float(), nullable=True)
    details_diameter_before: Mapped[float | None] = Column(Float(), nullable=True)
    welding_equipment: Mapped[str | None] = Column(String(), nullable=True)

    welder: Mapped[WelderModel] = relationship("WelderModel", back_populates="certifications")


class NDTModel(Base):
    __tablename__ = "ndt_table"
    
    ident: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    kleymo: Mapped[str] = Column(String(4), ForeignKey("welder_table.kleymo", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    company: Mapped[str | None] = Column(String(), nullable=True)
    subcompany: Mapped[str | None] = Column(String(), nullable=True)
    project: Mapped[str | None] = Column(String(), nullable=True)
    welding_date: Mapped[date] = Column(Date(), nullable=False)
    total_weld_1: Mapped[float | None] = Column(Float(), nullable=True)
    total_ndt_1: Mapped[float | None] = Column(Float(), nullable=True)
    total_accepted_1: Mapped[float | None] = Column(Float(), nullable=True)
    total_repair_1: Mapped[float | None] = Column(Float(), nullable=True)
    repair_status_1: Mapped[float | None] = Column(Float(), nullable=True)
    total_weld_2: Mapped[float | None] = Column(Float(), nullable=True)
    total_ndt_2: Mapped[float | None] = Column(Float(), nullable=True)
    total_accepted_2: Mapped[float | None] = Column(Float(), nullable=True)
    total_repair_2: Mapped[float | None] = Column(Float(), nullable=True)
    repair_status_2: Mapped[float | None] = Column(Float(), nullable=True)
    total_weld_3: Mapped[float | None] = Column(Float(), nullable=True)
    total_ndt_3: Mapped[float | None] = Column(Float(), nullable=True)
    total_accepted_3: Mapped[float | None] = Column(Float(), nullable=True)
    total_repair_3: Mapped[float | None] = Column(Float(), nullable=True)
    repair_status_3: Mapped[float | None] = Column(Float(), nullable=True)
    
    welder: Mapped[WelderModel] = relationship("WelderModel", back_populates="ndts")
