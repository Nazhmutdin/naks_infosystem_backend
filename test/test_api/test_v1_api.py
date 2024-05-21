import typing as t
import json

import pytest

from client import client
from shemas import *
from shemas import WelderCertificationShema


@pytest.mark.usefixtures("prepare_db")
class BaseTestCRUDEndpoints[Shema: BaseShema]:
    __shema__: type[Shema]

    def test_add(self, api_path, shema: Shema):
        res = client.post(api_path, json=shema.model_dump(mode="json"))

        assert res.status_code == 200

        assert type(shema).model_validate(json.loads(res.text)["data"]) == shema


    def test_get(self, api_path: str, shema: Shema): 
        res = client.get(api_path)

        assert shema == type(shema).model_validate(json.loads(res.text)) 

    
    def test_update(self, api_path: str, data: Shema):

        res = client.patch(api_path, json=data.model_dump(mode="json", exclude_unset=True))

        assert res.status_code == 200

        shema = client.get(api_path)

        assert shema.status_code == 200

        shema = self.__shema__.model_validate(json.loads(shema.text)).model_dump()

        for key, value in data.model_dump(exclude_unset=True).items():
            assert shema[key] == value


    def test_delete(self, api_path: str, shema: Shema): 
        res = client.delete(f"{api_path}/{shema.ident.hex}")

        assert res.status_code == 200

        res = client.get(f"{api_path}/{shema.ident.hex}")

        assert "not found" in json.loads(res.text)["detail"]
        
        res = client.post(api_path, json=shema.model_dump(mode="json"))


class TestWelderCRUDEndpoints(BaseTestCRUDEndpoints[WelderShema]):
    __shema__ = WelderShema

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
            "ident, data",
            [
                (
                    "d0099cbcb62345c2bc28a527642ab39c", 
                    {
                        "kleymo": "8M8S",
                        "name": "Йадав Аджай",
                        "birthday": "2000.01.01",
                        "passport_number": "55442233",
                    }
                ),
                (
                    "BKFC", 
                    {
                        "name": "Моханан Сануп",
                        "sicil": "126542",
                        "nation": "RUS",
                    }
                )
            ]
    )
    def test_update(self, ident: str, data: dict[str, t.Any]):
        return super().test_update(
            f"/api/v1/welders/{ident}",
            UpdateWelderShema.model_validate(data)
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
    __shema__ = WelderCertificationShema

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
            "ident, data",
            [
                (
                    "eac5ab3126ef48ac9e3d45022bb4571b", 
                    {
                        "details_thikness_from": 2,
                        "joint_type": [
                            "УШ",
                            "СШ"
                        ],
                        "kleymo": "B2MV",
                    }
                ),
                (
                    "4d061eb7bf9a4a16913223ea3926aa19", 
                    {
                        "welding_materials_groups": [
                            "M01",
                            "M03+M011",
                            "M03"
                        ],
                        "outer_diameter_from": 157.0,
                        "expiration_date_fact": "2022-04-05",
                    }
                )
            ]
    )
    def test_update(self, ident: str, data: dict[str, t.Any]):
        return super().test_update(
            f"/api/v1/welder-certifications/{ident}",
            UpdateWelderCertificationShema.model_validate(data)
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


class TestNDTCRUDEndpoints(BaseTestCRUDEndpoints[NDTShema]):
    __shema__ = NDTShema

    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3, 4]
    )
    @pytest.mark.usefixtures("test_ndts")
    def test_add(self, index: int, test_ndts: list[NDTShema]):
        ndt = test_ndts[index]

        return super().test_add(
            f"/api/v1/ndts",
            ndt
        )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("test_ndts")
    def test_get(self, index: int, test_ndts: list[NDTShema]):
        ndt = test_ndts[index]

        return super().test_get(
            f"/api/v1/ndts/{ndt.ident.hex}",
            ndt
        )
    

    @pytest.mark.parametrize(
            "ident, data",
            [
                (
                    "415e23fbd655402bb99b96868f4ec2d5", 
                    {
                        "total_weld_2": 4255.0,
                        "total_ndt_2": 306.0,
                        "total_accepted_2": 30118.0,
                    }
                ),
                (
                    "778fd525f17e4c1c9f929adfca0ad300", 
                    {
                        "comp": "PIRAM",
                        "subcon": "PIRAMITd122",
                        "project": "AWP1Bdwe",
                        "welding_date": "2022-05-17"
                    }
                )
            ]
    )
    def test_update(self, ident: str, data: dict[str, t.Any]):
        return super().test_update(
            f"/api/v1/ndts/{ident}",
            UpdateNDTShema.model_validate(data)
        )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("test_ndts")
    def test_delete(self, index: int, test_ndts: list[NDTShema]):
        ndt = test_ndts[index]

        return super().test_delete(
            f"/api/v1/ndts",
            ndt
        )
