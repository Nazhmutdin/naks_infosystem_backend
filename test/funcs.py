import json

from shemas import *


def get_personals() -> list[PersonalShema]:
    personals = json.load(open("test/test_data/personals.json", "r", encoding="utf-8"))
    return [PersonalShema(**personal) for personal in personals]


def get_personal_certifications() -> list[PersonalCertificationShema]:
    certifications = json.load(open("test/test_data/personal_certifications.json", "r", encoding="utf-8"))
    return [PersonalCertificationShema(**certification) for certification in certifications]


def get_ndts() -> list[NDTShema]:
    ndts = json.load(open("test/test_data/ndts.json", "r", encoding="utf-8"))
    return [NDTShema(**ndt) for ndt in ndts]
