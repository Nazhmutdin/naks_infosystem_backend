from dataclasses import dataclass

from sqlalchemy import join, desc
from naks_library.selector_filters import InFilter, FromFilter, BeforeFilter, ILikeAnyFilter, AbstractFilter, EqualFilter

from app.infrastructure.database.models import PersonalModel, PersonalNaksCertificationModel, NdtModel, AcstModel

PERSONAL_FILTERS_MAP: dict[str, AbstractFilter] = {
    "idents": InFilter(PersonalModel.ident),
    "naks_certification_idents": InFilter(PersonalNaksCertificationModel.ident),
    "names": ILikeAnyFilter(PersonalModel.name),
    "kleymos": InFilter(PersonalModel.kleymo),
    "naks_certification_numbers": InFilter(PersonalNaksCertificationModel.certification_number),
    "inserts": InFilter(PersonalNaksCertificationModel.insert),
    "methods": InFilter(PersonalNaksCertificationModel.method),
    "certification_date_from": FromFilter(PersonalNaksCertificationModel.certification_date),
    "certification_date_before": BeforeFilter(PersonalNaksCertificationModel.certification_date),
    "expiration_date_from": FromFilter(PersonalNaksCertificationModel.expiration_date),
    "expiration_date_before": BeforeFilter(PersonalNaksCertificationModel.expiration_date),
    "expiration_date_fact_from": FromFilter(PersonalNaksCertificationModel.expiration_date_fact),
    "expiration_date_fact_before": BeforeFilter(PersonalNaksCertificationModel.expiration_date_fact)
}


PERSONAL_SELECT_ATTRS = [
    PersonalModel
]


PERSONAL_SELECT_FROM_ATTRS = [
    join(PersonalModel, PersonalNaksCertificationModel)
]

PERSONAL_ORDER_BY_ATTRS = [
    PersonalModel.ident
]


@dataclass
class PersonalSelectStmtCreatorConfig:
    filters_map = PERSONAL_FILTERS_MAP
    select_attrs = PERSONAL_SELECT_ATTRS
    select_from_attrs = PERSONAL_SELECT_FROM_ATTRS
    order_by_attrs = PERSONAL_ORDER_BY_ATTRS


PERSONAL_NAKS_CERTIFICATION_FILTERS_MAP: dict[str, AbstractFilter] = {
    "idents": InFilter(PersonalNaksCertificationModel.ident),
    "personal_idents": InFilter(PersonalNaksCertificationModel.personal_ident),
    "certification_numbers": InFilter(PersonalNaksCertificationModel.certification_number),
    "inserts": InFilter(PersonalNaksCertificationModel.insert),
    "methods": InFilter(PersonalNaksCertificationModel.method),
    "certification_date_from": FromFilter(PersonalNaksCertificationModel.certification_date),
    "certification_date_before": BeforeFilter(PersonalNaksCertificationModel.certification_date),
    "expiration_date_from": FromFilter(PersonalNaksCertificationModel.expiration_date),
    "expiration_date_before": BeforeFilter(PersonalNaksCertificationModel.expiration_date),
    "expiration_date_fact_from": FromFilter(PersonalNaksCertificationModel.expiration_date_fact),
    "expiration_date_fact_before": BeforeFilter(PersonalNaksCertificationModel.expiration_date_fact)
}


PERSONAL_NAKS_CERTIFICATION_SELECT_ATTRS = [
    PersonalNaksCertificationModel
]


PERSONAL_NAKS_CERTIFICATION_SELECT_FROM_ATTRS = [
    PersonalNaksCertificationModel
]

PERSONAL_NAKS_CERTIFICATION_ORDER_BY_ATTRS = [
    desc(PersonalNaksCertificationModel.expiration_date_fact)
]


@dataclass
class PersonalNaksCertificationSelectStmtCreatorConfig:
    filters_map = PERSONAL_NAKS_CERTIFICATION_FILTERS_MAP
    select_attrs = PERSONAL_NAKS_CERTIFICATION_SELECT_ATTRS
    select_from_attrs = PERSONAL_NAKS_CERTIFICATION_SELECT_FROM_ATTRS
    order_by_attrs = PERSONAL_NAKS_CERTIFICATION_ORDER_BY_ATTRS


NDT_FILTERS_MAP: dict[str, AbstractFilter] = {
    "idents": InFilter(NdtModel.ident),
    "personal_idents": InFilter(NdtModel.personal_ident),
    "welding_date_from": FromFilter(NdtModel.welding_date),
    "welding_date_before": BeforeFilter(NdtModel.welding_date),
    "total_welded_from": FromFilter(NdtModel.total_welded),
    "total_welded_before": BeforeFilter(NdtModel.total_welded),
    "total_ndt_from": FromFilter(NdtModel.total_ndt),
    "total_ndt_before": BeforeFilter(NdtModel.total_ndt),
    "total_accepted_from": FromFilter(NdtModel.total_accepted),
    "total_accepted_before": BeforeFilter(NdtModel.total_accepted),
    "total_rejected_from": FromFilter(NdtModel.total_rejected),
    "total_rejected_before": BeforeFilter(NdtModel.total_rejected)
}


NDT_SELECT_ATTRS = [
    NdtModel
]


NDT_SELECT_FROM_ATTRS = [
    NdtModel
]


NDT_ORDER_BY_ATTRS = [
    desc(NdtModel.welding_date)
]


@dataclass
class NdtSelectStmtCreatorConfig:
    filters_map = NDT_FILTERS_MAP
    select_attrs = NDT_SELECT_ATTRS
    select_from_attrs = NDT_SELECT_FROM_ATTRS
    order_by_attrs = NDT_ORDER_BY_ATTRS


ACST_FILTERS_MAP: dict[str, AbstractFilter] = {
    "idents": InFilter(AcstModel.ident),
    "acst_numbers": InFilter(AcstModel.acst_number),
    "certification_date_from": FromFilter(AcstModel.certification_date),
    "certification_date_before": BeforeFilter(AcstModel.certification_date),
    "expiration_date_from": FromFilter(AcstModel.expiration_date),
    "expiration_date_before": BeforeFilter(AcstModel.expiration_date),
    "thikness_from": FromFilter(AcstModel.thikness_from),
    "thikness_before": BeforeFilter(AcstModel.thikness_before),
    "diameter_from": FromFilter(AcstModel.diameter_from),
    "diameter_before": BeforeFilter(AcstModel.diameter_before),
    "preheating": EqualFilter(AcstModel.preheating),
    "heat_treatment": EqualFilter(AcstModel.heat_treatment),
    "gtds": InFilter(AcstModel.gtd),
    "methods": InFilter(AcstModel.method)
}


ACST_SELECT_ATTRS = [
    AcstModel
]

ACST_SELECT_FROM_ATTRS = [
    AcstModel
]

ACST_ORDER_BY_ATTRS = [
    desc(AcstModel.expiration_date)
]


@dataclass
class AcstSelectStmtCreatorConfig:
    filters_map = ACST_FILTERS_MAP
    select_attrs = ACST_SELECT_ATTRS
    select_from_attrs = ACST_SELECT_FROM_ATTRS
    order_by_attrs = ACST_ORDER_BY_ATTRS
