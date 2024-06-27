import json

from shemas import *


def get_welders() -> list[WelderShema]:
    welders = json.load(open("test/test_data/welders.json", "r", encoding="utf-8"))
    return [WelderShema.model_validate(welder) for welder in welders]


def get_welder_certifications() -> list[WelderCertificationShema]:
    certifications = json.load(open("test/test_data/welder_certifications.json", "r", encoding="utf-8"))
    return [WelderCertificationShema.model_validate(certification) for certification in certifications]


def get_ndts() -> list[NDTShema]:
    ndts = json.load(open("test/test_data/ndts.json", "r", encoding="utf-8"))
    return [NDTShema.model_validate(ndt) for ndt in ndts]