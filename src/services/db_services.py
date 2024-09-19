from sqlalchemy import join
from sqlalchemy.orm.attributes import InstrumentedAttribute
from naks_library.base_db_service import BaseDBService
from naks_library.utils import AbstractFilter, BeforeFilter, FromFilter, InFilter, ILikeAnyFilter

from src.shemas import *
from src.models import PersonalModel, PersonalCertificationModel, NDTModel
from src._types import PersonalData, PersonalCertificationData, NDTData


__all__: list[str] = [
    "PersonalDBService",
    "PersonalCertificationDBService",
    "NDTDBService"
]


PERSONAL_FILTERS_MAP: dict[str, AbstractFilter] = {
    "idents": InFilter(PersonalModel.ident),
    "certification_idents": InFilter(PersonalCertificationModel.ident),
    "names": ILikeAnyFilter(PersonalModel.name),
    "kleymos": InFilter(PersonalModel.kleymo),
    "certification_numbers": InFilter(PersonalCertificationModel.certification_number),
    "inserts": InFilter(PersonalCertificationModel.insert),
    "methods": InFilter(PersonalCertificationModel.method),
    "certification_date_from": FromFilter(PersonalCertificationModel.certification_date),
    "certification_date_before": BeforeFilter(PersonalCertificationModel.certification_date),
    "expiration_date_from": FromFilter(PersonalCertificationModel.expiration_date),
    "expiration_date_before": BeforeFilter(PersonalCertificationModel.expiration_date),
    "expiration_date_fact_from": FromFilter(PersonalCertificationModel.expiration_date_fact),
    "expiration_date_fact_before": BeforeFilter(PersonalCertificationModel.expiration_date_fact)
}


PERSONAL_SELECT_ATTRS = [
    PersonalModel
]


PERSONAL_SELECT_FROM_ATTRS = [
    join(PersonalModel, PersonalCertificationModel)
]


PERSONAL_OR_SELECT_COLUMNS: list[InstrumentedAttribute] = [
    PersonalModel.ident,
    PersonalModel.kleymo,
    PersonalCertificationModel.certification_number,
    PersonalModel.name,
    PersonalCertificationModel.ident
]


PERSONAL_AND_SELECT_COLUMNS: list[InstrumentedAttribute] = [
    PersonalCertificationModel.certification_date,
    PersonalCertificationModel.expiration_date,
    PersonalCertificationModel.expiration_date_fact,
    PersonalCertificationModel.certification_number,
    PersonalCertificationModel.method,
    PersonalCertificationModel.insert,
]


class PersonalDBService(BaseDBService[PersonalData, PersonalModel, PersonalSelectShema, CreatePersonalShema, UpdatePersonalShema]):

    def __init__(self):
        self.__dto__ = PersonalData
        self.__model__ = PersonalModel
        self._filters_map = PERSONAL_FILTERS_MAP
        self._select_attrs = PERSONAL_SELECT_ATTRS
        self._select_from_attrs = PERSONAL_SELECT_FROM_ATTRS
        self._and_model_columns = PERSONAL_AND_SELECT_COLUMNS
        self._or_model_columns = PERSONAL_OR_SELECT_COLUMNS


PERSONAL_CERTIFICATION_FILTERS_MAP: dict[str, AbstractFilter] = {
    "idents": InFilter(PersonalCertificationModel.ident),
    "personal_idents": InFilter(PersonalCertificationModel.personal_ident),
    "certification_numbers": InFilter(PersonalCertificationModel.certification_number),
    "inserts": InFilter(PersonalCertificationModel.insert),
    "methods": InFilter(PersonalCertificationModel.method),
    "certification_date_from": FromFilter(PersonalCertificationModel.certification_date),
    "certification_date_before": BeforeFilter(PersonalCertificationModel.certification_date),
    "expiration_date_from": FromFilter(PersonalCertificationModel.expiration_date),
    "expiration_date_before": BeforeFilter(PersonalCertificationModel.expiration_date),
    "expiration_date_fact_from": FromFilter(PersonalCertificationModel.expiration_date_fact),
    "expiration_date_fact_before": BeforeFilter(PersonalCertificationModel.expiration_date_fact)
}


PERSONAL_CERTIFICATION_SELECT_ATTRS = [
    PersonalCertificationModel
]


PERSONAL_CERTIFICATION_SELECT_FROM_ATTRS = [
    PersonalCertificationModel
]


PERSONAL_CERTIFICATION_OR_SELECT_COLUMNS: list[InstrumentedAttribute] = [
    PersonalCertificationModel.certification_number,
    PersonalCertificationModel.personal_ident,
    PersonalCertificationModel.ident
]


PERSONAL_CERTIFICATION_AND_SELECT_COLUMNS: list[InstrumentedAttribute] = [
    PersonalCertificationModel.certification_date,
    PersonalCertificationModel.expiration_date,
    PersonalCertificationModel.expiration_date_fact,
    PersonalCertificationModel.certification_number,
    PersonalCertificationModel.method,
    PersonalCertificationModel.insert,
]


class PersonalCertificationDBService(BaseDBService[PersonalCertificationData, PersonalCertificationModel, PersonalCertificationSelectShema, CreatePersonalCertificationShema, UpdatePersonalCertificationShema]):
    def __init__(self):
        self.__dto__ = PersonalCertificationData
        self.__model__ = PersonalCertificationModel
        self._filters_map = PERSONAL_CERTIFICATION_FILTERS_MAP
        self._select_attrs = PERSONAL_CERTIFICATION_SELECT_ATTRS
        self._select_from_attrs = PERSONAL_CERTIFICATION_SELECT_FROM_ATTRS
        self._and_model_columns = PERSONAL_CERTIFICATION_AND_SELECT_COLUMNS
        self._or_model_columns = PERSONAL_CERTIFICATION_OR_SELECT_COLUMNS


NDT_FILTERS_MAP: dict[str, AbstractFilter] = {
    "idents": InFilter(NDTModel.ident),
    "personal_idents": InFilter(NDTModel.personal_ident),
    "welding_date_from": FromFilter(PersonalCertificationModel.certification_date),
    "welding_date_before": BeforeFilter(PersonalCertificationModel.certification_date),
    "total_welded_from": FromFilter(PersonalCertificationModel.expiration_date),
    "total_welded_before": BeforeFilter(PersonalCertificationModel.expiration_date),
    "total_ndt_from": FromFilter(PersonalCertificationModel.expiration_date_fact),
    "total_ndt_before": BeforeFilter(PersonalCertificationModel.expiration_date_fact),
    "total_accepted_from": FromFilter(PersonalCertificationModel.expiration_date_fact),
    "total_accepted_before": BeforeFilter(PersonalCertificationModel.expiration_date_fact),
    "total_rejected_from": FromFilter(PersonalCertificationModel.expiration_date_fact),
    "total_rejected_before": BeforeFilter(PersonalCertificationModel.expiration_date_fact)
}


NDT_SELECT_ATTRS = [
    NDTModel
]


NDT_SELECT_FROM_ATTRS = [
    NDTModel
]


NDT_OR_SELECT_COLUMNS: list[InstrumentedAttribute] = [
    NDTModel.ident,
    NDTModel.personal_ident
]


NDT_AND_SELECT_COLUMNS: list[InstrumentedAttribute] = [
    NDTModel.welding_date,
    NDTModel.total_welded,
    NDTModel.total_ndt,
    NDTModel.total_accepted,
    NDTModel.total_rejected,
    NDTModel.ndt_type
]


class NDTDBService(BaseDBService[NDTData, NDTModel, NDTSelectShema, CreateNDTShema, UpdateNDTShema]):
    def __init__(self):
        self.__dto__ = NDTData
        self.__model__ = NDTModel
        self._filters_map = NDT_FILTERS_MAP
        self._select_attrs = NDT_SELECT_ATTRS
        self._select_from_attrs = NDT_SELECT_FROM_ATTRS
        self._and_model_columns = NDT_AND_SELECT_COLUMNS
        self._or_model_columns = NDT_OR_SELECT_COLUMNS
