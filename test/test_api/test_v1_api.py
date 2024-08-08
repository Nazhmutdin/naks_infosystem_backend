import typing as t
import json

import pytest
from naks_library import BaseShema

from services.db_services import *
from client import client
from utils.DTOs import *
from shemas import *
from funcs import test_data


class BaseTestCRUDEndpoints[DTO, Shema: BaseShema]:
    __dto__: type[DTO]
    __shema__: type[Shema]

    def test_add(self, api_path, item: Shema):
        res = client.post(api_path, json=item.model_dump(mode="json"))

        assert res.status_code == 200


    def test_get(self, api_path: str, item: DTO): 
        res = client.get(api_path)

        assert item == self.__dto__(**json.loads(res.text)) 

    
    def test_update(self, api_path: str, data: Shema):
        res = client.patch(api_path, json=data.model_dump(mode="json", exclude_unset=True))

        assert res.status_code == 200

        res = client.get(api_path)

        assert res.status_code == 200

        result = self.__shema__.model_validate(json.loads(res.text))

        for key, value in data.__dict__.items():
            assert getattr(result, key) == value


    def test_delete(self, api_path: str, item: DTO): 
        res = client.delete(f"{api_path}/{item.ident}")

        assert res.status_code == 200

        res = client.get(f"{api_path}/{item.ident.hex}")

        assert "not found" in json.loads(res.text)["detail"]
        
        res = client.post(api_path, json=json.loads(json.dumps(item.__dict__, default=str)))

        assert res.status_code == 200


class TestPersonalCRUDEndpoints(BaseTestCRUDEndpoints):
    __shema__ = PersonalShema
    __dto__ = PersonalData


    @pytest.mark.usefixtures("personals")
    def test_add(self, personals: list[PersonalData]):
        for personal in personals:

            super().test_add(
                f"/v1/personal",
                CreatePersonalShema.model_validate(personal.__dict__)
            )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("personals")
    def test_get(self, index: int, personals: list[PersonalData]):
        personal = personals[index]

        return super().test_get(
            f"/v1/personal/{personal.ident.hex}",
            personal
        )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("personals")
    def test_get_by_kleymo(self, index: int, personals: list[PersonalData]):
        personal = personals[index]

        return super().test_get(
            f"/v1/personal/{personal.kleymo}",
            personal
        )
    

    @pytest.mark.parametrize(
        "ident, data",
        [(personal.ident, new_personal_data) for personal, new_personal_data in zip(test_data.fake_personals[:5], test_data.fake_personal_generator.generate(5))]
    )
    def test_update(self, ident: str, data: dict[str, t.Any]):
        return super().test_update(
            f"v1/personal/{ident}",
            UpdatePersonalShema.model_validate(data)
        )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("personals")
    def test_delete(self, index: int, personals: list[PersonalData]):
        personal = personals[index]

        return super().test_delete(
            f"/v1/personal",
            CreatePersonalShema.model_validate(personal.__dict__)
        )


class TestPersonalCertificationCRUDEndpoints(BaseTestCRUDEndpoints):
    __shema__ = PersonalCertificationShema
    __dto__ = PersonalCertificationData

    
    @pytest.mark.usefixtures("personal_certifications")
    def test_add(self, personal_certifications: list[PersonalCertificationData]): 
        for certification in personal_certifications[:5]:
            super().test_add(
                f"/v1/personal-certification",
                CreatePersonalCertificationShema.model_validate(certification.__dict__)
            )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("personal_certifications")
    def test_get(self, index: int, personal_certifications: list[PersonalCertificationData]):
        certification = personal_certifications[index]

        return super().test_get(
            f"/v1/personal-certification/{certification.ident.hex}",
            certification
        )
    

    @pytest.mark.parametrize(
        "ident, data",
        [(personal_certification.ident, new_personal_certification_data) for personal_certification, new_personal_certification_data in zip(test_data.fake_personal_certifications[:5], test_data.fake_personal_certification_generator.generate(5))]
    )
    def test_update(self, ident: str, data: dict[str, t.Any]):
        return super().test_update(
            f"/v1/personal-certification/{ident}",
            UpdatePersonalCertificationShema.model_validate(data)
        )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("personal_certifications")
    def test_delete(self, index: int, personal_certifications: list[PersonalCertificationData]):
        certification = personal_certifications[index]

        return super().test_delete(
            f"/v1/personal-certification",
            CreatePersonalCertificationShema.model_validate(certification.__dict__)
        )


class TestNDTCRUDEndpoints(BaseTestCRUDEndpoints):
    __shema__ = NDTShema
    __dto__ = NDTData


    @pytest.mark.usefixtures("ndts")
    def test_add(self, ndts: list[NDTData]):

        for ndt in ndts[:5]:

            super().test_add(
                f"/v1/ndt",
                CreateNDTShema.model_validate(ndt.__dict__)
            )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("ndts")
    def test_get(self, index: int, ndts: list[NDTData]):
        ndt = ndts[index]

        return super().test_get(
            f"/v1/ndt/{ndt.ident.hex}",
            ndt
        )
    

    @pytest.mark.parametrize(
        "ident, data",
        [(ndt.ident, new_ndt_data) for ndt, new_ndt_data in zip(test_data.fake_ndts[:5], test_data.fake_ndt_generator.generate(5))]
    )
    def test_update(self, ident: str, data: dict[str, t.Any]):
        return super().test_update(
            f"/v1/ndt/{ident}",
            UpdateNDTShema.model_validate(data)
        )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("ndts")
    def test_delete(self, index: int, ndts: list[NDTData]):
        ndt = ndts[index]

        return super().test_delete(
            f"/v1/ndt",
            CreateNDTShema.model_validate(ndt.__dict__)
        )
