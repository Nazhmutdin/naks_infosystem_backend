import typing as t
import json

import pytest

from client import client
from shemas import *
from shemas import WelderShema


@pytest.mark.usefixtures("prepare_db")
class BaseTestCRUDEndpoints[Shema: BaseShema]:

    def test_add(self, api_path, shema: Shema):
        res = client.post(api_path, json=shema.model_dump(mode="json"))

        assert res.status_code == 200

        res = client.get(f"{api_path}/{shema.ident}")

        assert res.status_code == 200

        assert type(shema).model_validate(json.loads(res.text)) == shema


    def test_get(self, api_path: str, shema: Shema): 
        res = client.get(api_path)

        assert shema == type(shema).model_validate(json.loads(res.text)) 


    def test_delete(self, api_path: str, shema: Shema): 
        res = client.delete(f"{api_path}/{shema.ident.hex}")

        assert res.status_code == 200

        res = client.get(f"{api_path}/{shema.ident.hex}")

        assert "not found" in json.loads(res.text)["detail"]
        
        res = client.post(api_path, json=shema.model_dump(mode="json"))


class TestWelderCRUDEndpoints(BaseTestCRUDEndpoints[WelderShema]):

    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("test_welders")
    def test_add(self, index: int, test_welders: list[WelderShema]):
        welder = test_welders[index]

        return super().test_add(
            f"/api/v1/welders",
            welder
        )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("test_welders")
    def test_get(self, index: int, test_welders: list[WelderShema]):
        welder = test_welders[index]

        return super().test_get(
            f"/api/v1/welders/{welder.ident.hex}",
            welder
        )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("test_welders")
    def test_get_by_kleymo(self, index: int, test_welders: list[WelderShema]):
        welder = test_welders[index]

        return super().test_get(
            f"/api/v1/welders/{welder.kleymo}",
            welder
        )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("test_welders")
    def test_delete(self, index: int, test_welders: list[WelderShema]):
        welder = test_welders[index]

        return super().test_delete(
            f"/api/v1/welders",
            welder
        )


class TestWelderCertificationCRUDEndpoints(BaseTestCRUDEndpoints[WelderCertificationShema]):

    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("test_welder_certifications")
    def test_add(self, index: int, test_welder_certifications: list[WelderCertificationShema]):
        certification = test_welder_certifications[index]

        return super().test_add(
            f"/api/v1/welder-certifications",
            certification
        )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("test_welder_certifications")
    def test_get(self, index: int, test_welder_certifications: list[WelderCertificationShema]):
        certification = test_welder_certifications[index]

        return super().test_get(
            f"/api/v1/welder-certifications/{certification.ident.hex}",
            certification
        )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("test_welder_certifications")
    def test_delete(self, index: int, test_welder_certifications: list[WelderCertificationShema]):
        certification = test_welder_certifications[index]

        return super().test_delete(
            f"/api/v1/welder-certifications",
            certification
        )
