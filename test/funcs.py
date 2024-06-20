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


def get_users() -> list[UserShema]:
    users = json.load(open("test/test_data/users.json", "r", encoding="utf-8"))
    return [UserShema.model_validate(user) for user in users]


def get_refresh_tokens() -> list[RefreshTokenShema]:
    tokens = json.load(open("test/test_data/refresh_tokens.json", "r", encoding="utf-8"))
    return [RefreshTokenShema.model_validate(token) for token in tokens]


def get_request_refresh_tokens() -> list[RefreshTokenShema]:
    tokens = json.load(open("test/test_data/request_refresh_tokens.json", "r", encoding="utf-8"))
    return tokens
