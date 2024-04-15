import typing as t
from re import fullmatch
from datetime import date
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

from errors import FieldValidationException
from utils.funcs import to_date


__all__: list[str] = [
    "BaseShema",
    "BaseWelderShema",
    "WelderShema",
    "CreateWelderShema",
    "UpdateWelderShema",
    "BaseWelderCertificationShema",
    "WelderCertificationShema",
    "CreateWelderCertificationShema",
    "UpdateWelderCertificationShema",
    "BaseNDTShema",
    "NDTShema",
    "CreateNDTShema",
    "UpdateNDTShema",
    # "EngineerShema",
    # "EngineerCertificationShema",
    # "UserShema",
]


class BaseShema(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        validate_assignment=True,
        revalidate_instances="always"
    )
    
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        
        self_dict = self.model_dump()

        for key, value in other.model_dump().items():
            if key == "ident": continue
            
            if key not in self_dict:
                return False
            
            if value != self_dict[key]:
                return False
        
        return True


"""
====================================================================================================
Welder shema
====================================================================================================
"""


class BaseWelderShema(BaseShema):
    kleymo: str | None = Field(default=None)
    name: str | None = Field(default=None)
    birthday: date | None = Field(default=None)
    passport_number: str | None = Field(default=None)
    sicil: str | None = Field(default=None)
    nation: str | None = Field(default=None)
    status: int = Field(default=0)


class WelderShema(BaseWelderShema):
    ident: UUID = Field(default_factory=uuid4)
    kleymo: str
    name: str
    
    @field_validator("ident")
    @classmethod
    def validate_ident(cls, v: str | UUID | None):
        if not v:
            return uuid4()
        elif isinstance(v, str):
            return UUID(v)
        
        return v

    @field_validator("kleymo")
    @classmethod
    def validate_kleymo(cls, v: str | int):
        
        if fullmatch(r"[A-Z0-9]{4}", v.strip()):
            return v
        
        raise FieldValidationException(f"Invalid kleymo: {v}")
    

    @field_validator("birthday")
    @classmethod
    def validate_birthday(cls, v: str | tuple[int, int, int] | None):
        try:
            return to_date(v)
        except:
            return None



    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v: int | str | None):
        if isinstance(v, str):
            try:
                return int(v)
            except:
                raise FieldValidationException(f"{v} cannot be converted to int")
            
        if not v:
            return 0
        
        return v


class CreateWelderShema(WelderShema): ...


class UpdateWelderShema(BaseWelderShema):

    @field_validator("kleymo")
    @classmethod
    def validate_kleymo(cls, v: str | int | None):
        if not v:
            return None
        
        if isinstance(v, int):
            v = str(v)
        
        if fullmatch(r"[A-Z0-9]{4}", v.strip()):
            return v
        
        raise FieldValidationException(f"Invalid kleymo: {v}")
    

    @field_validator("birthday", mode="before")
    @classmethod
    def validate_birthday(cls, v: str | tuple[int, int, int] | None):
        try:
            return to_date(v)
        except:
            return None


"""
====================================================================================================
Welder certification shema
====================================================================================================
"""


class BaseWelderCertificationShema(BaseShema):
    kleymo: str | None = Field(default=None)
    job_title: str | None = Field(default=None)
    certification_number: str | None = Field(default=None)
    certification_date: date | None = Field(default=None)
    expiration_date: date | None = Field(default=None)
    expiration_date_fact: date | None = Field(default=None)
    insert: str | None = Field(default=None)
    certification_type: str | None = Field(default=None)
    company: str | None = Field(default=None)
    gtd: list[str] | None = Field(default=None)
    method: str | None = Field(default=None)
    details_type: list[str] | None = Field(default=None)
    joint_type: list[str] | None = Field(default=None)
    welding_materials_groups: list[str] | None = Field(default=None)
    welding_materials: str | None = Field(default=None)
    details_thikness_from: float | None = Field(default=None)
    details_thikness_before: float | None = Field(default=None)
    outer_diameter_from: float | None = Field(default=None)
    outer_diameter_before: float | None = Field(default=None)
    welding_position: str | None = Field(default=None)
    connection_type: str | None = Field(default=None)
    rod_diameter_from: float | None = Field(default=None)
    rod_diameter_before: float | None = Field(default=None)
    rod_axis_position: str | None = Field(default=None)
    weld_type: str | None = Field(default=None)
    joint_layer: str | None = Field(default=None)
    sdr: str | None = Field(default=None)
    automation_level: str | None = Field(default=None)
    details_diameter_from: float | None = Field(default=None)
    details_diameter_before: float | None = Field(default=None)
    welding_equipment: str | None = Field(default=None)


    def short_model_dump(self) -> dict[str, t.Any]:
        res = {}

        for key, value in self.model_dump().items():
            if key in ["kleymo", "ident", "certification_number", "certification_date", "expiration_date_fact", "insert", "method"]:
                res[key] = value

        return res


class WelderCertificationShema(BaseWelderCertificationShema):
    ident: UUID = Field(default_factory=uuid4)
    kleymo: str = Field()
    certification_number: str = Field()
    certification_date: date = Field()
    expiration_date: date = Field()
    expiration_date_fact: date = Field()


    @field_validator("kleymo")
    @classmethod
    def validate_kleymo(cls, v: str | int | None):
        if not v:
            return FieldValidationException(f"kleymo is required")
        
        if isinstance(v, int):
            v = str(v)
        
        if fullmatch(r"[A-Z0-9]{4}", v.strip()):
            return v
        
        raise FieldValidationException(f"Invalid kleymo: {v}")
    
    
    @field_validator("certification_date", "expiration_date", "expiration_date_fact", mode="before")
    @classmethod
    def validate_date(cls, v: str | tuple[int, int, int] | None):
        if not v:
            raise FieldValidationException(f"Invalid date data '{v}'")
        
        try:
            return to_date(v)
        except:
            raise FieldValidationException(f"Invalid date data '{v}'")



class CreateWelderCertificationShema(WelderCertificationShema): ...


class UpdateWelderCertificationShema(BaseWelderCertificationShema): 

    @field_validator("kleymo")
    @classmethod
    def validate_kleymo(cls, v: str | int | None):
        if not v:
            return None
        
        if isinstance(v, int):
            v = str(v)
        
        if fullmatch(r"[A-Z0-9]{4}", v.strip()):
            return v
        
        raise FieldValidationException(f"Invalid kleymo: {v}")
    
    
    @field_validator("certification_date", "expiration_date", "expiration_date_fact", mode="before")
    @classmethod
    def validate_date(cls, v: str | tuple[int, int, int] | None):
        try:
            return to_date(v)
        except:
            raise FieldValidationException(f"Invalid date data '{v}'")
        

"""
====================================================================================================
NDT shema
====================================================================================================
"""


class BaseNDTShema(BaseShema):
    kleymo: str | None = Field(default=None)
    company: str | None = Field(default=None)
    subcompany: str | None = Field(default=None)
    project: str | None = Field(default=None)
    welding_date: date | None = Field(default=None)
    total_weld_1: float | None = Field(default=None)
    total_ndt_1: float | None = Field(default=None)
    total_accepted_1: float | None = Field(default=None)
    total_repair_1: float | None = Field(default=None)
    repair_status_1: float | None = Field(default=None)
    total_weld_2: float | None = Field(default=None)
    total_ndt_2: float | None = Field(default=None)
    total_accepted_2: float | None = Field(default=None)
    total_repair_2: float | None = Field(default=None)
    repair_status_2: float | None = Field(default=None)
    total_weld_3: float | None = Field(default=None)
    total_ndt_3: float | None = Field(default=None)
    total_accepted_3: float | None = Field(default=None)
    total_repair_3: float | None = Field(default=None)
    repair_status_3: float | None = Field(default=None)


    def short_model_dump(self) -> dict[str, t.Any]:
        res = {}

        for key, value in self.model_dump().items():
            if key in ["kleymo", "company", "subcompany", "project", "welding_date", "repair_status_1", "repair_status_2", "repair_status_3"]:
                res[key] = value
                
        return res


class NDTShema(BaseNDTShema):
    ident: UUID = Field(default_factory=uuid4)
    kleymo: str = Field()
    welding_date: date = Field()


    @field_validator("welding_date", mode="before")
    def validate_welding_date(cls, v: str | tuple[int, int, int] | None):
        if not v:
            raise FieldValidationException(f"Invalid date data '{v}'")
        
        try:
            return to_date(v)
        except:
            raise FieldValidationException(f"Invalid date data '{v}'")


    @field_validator("kleymo")
    @classmethod
    def validate_kleymo(cls, v: str | int | None):
        if not v:
            return None
        
        if isinstance(v, int):
            v = str(v)
        
        if fullmatch(r"[A-Z0-9]{4}", v.strip()):
            return v
        
        raise FieldValidationException(f"Invalid kleymo: {v}")


class CreateNDTShema(NDTShema): ...


class UpdateNDTShema(BaseNDTShema): 

    @field_validator("welding_date", mode="before")
    def validate_welding_date(cls, v: str | tuple[int, int, int] | None):
        try:
            return to_date(v)
        except:
            raise FieldValidationException(f"Invalid date data '{v}'")
        

    @field_validator("kleymo")
    @classmethod
    def validate_kleymo(cls, v: str | int | None):
        if not v:
            return None
        
        if isinstance(v, int):
            v = str(v)
        
        if fullmatch(r"[A-Z0-9]{4}", v.strip()):
            return v
        
        raise FieldValidationException(f"Invalid kleymo: {v}")