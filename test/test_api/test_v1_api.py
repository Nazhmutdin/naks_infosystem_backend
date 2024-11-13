import typing as t
import json

import pytest
from naks_library import BaseShema

from client import client
from funcs import test_data

from app.application.dto import (
    PersonalDTO, 
    PersonalNaksCertificationDTO, 
    NdtDTO
)
from app.presentation.shemas.personal import CreatePersonalShema, UpdatePersonalShema
from app.presentation.shemas.personal_naks_certification import CreatePersonalNaksCertificationShema, UpdatePersonalNaksCertificationShema
from app.presentation.shemas.ndt import CreateNdtShema, UpdateNdtShema


_Shema = t.TypeVar("_Shema", bound=BaseShema)
_DTO = t.TypeVar("_DTO", bound=BaseShema)


class BaseTestCRUDEndpoints:
    __dto__: type[_DTO]
    __update_shema__: type[_Shema]
    __create_shema__: type[_Shema]


    def test_add(self, api_path, item: _Shema):
        res = client.post(api_path, json=item.model_dump(mode="json"))

        assert res.status_code == 200


    def test_get(self, api_path: str, item: _DTO):
        res = client.get(api_path)

        sub_data = json.loads(res.text)

        assert item.__dict__ == self.__create_shema__.model_validate(sub_data).__dict__

    
    def test_update(self, api_path: str, data: _Shema):
        res = client.patch(api_path, json=data.model_dump(mode="json", exclude_unset=True))

        assert res.status_code == 200

        res = client.get(api_path)

        assert res.status_code == 200

        result: dict = json.loads(res.text)

        for key, value in data.model_dump(mode="json", by_alias=True).items():
            assert result.get(key, None) == value


    def test_delete(self, api_path: str, item: _Shema): 
        res = client.delete(f"{api_path}/{item.ident}")

        assert res.status_code == 200

        assert client.get(f"{api_path}/{item.ident}").status_code == 404
        
        res = client.post(api_path, json=item.model_dump(mode="json"))

        assert res.status_code == 200


class TestPersonalCRUDEndpoints(BaseTestCRUDEndpoints):
    __update_shema__ = UpdatePersonalShema
    __create_shema__ = CreatePersonalShema
    __dto__ = PersonalDTO


    @pytest.mark.usefixtures("personals")
    def test_add(self, personals: list[PersonalDTO]):
        for personal in personals:

            super().test_add(
                "/v1/personal",
                self.__create_shema__.model_validate(personal.__dict__)
            )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("personals")
    def test_get(self, index: int, personals: list[PersonalDTO]):

        personal = personals[index]

        return super().test_get(
            f"/v1/personal/{personal.ident.hex}",
            personal
        )

    @pytest.mark.parametrize(
        "ident, data",
        [(personal.ident, new_personal_data) for personal, new_personal_data in zip(test_data.fake_personals[:5], test_data.fake_personal_generator.generate(5))]
    )
    def test_update(self, ident: str, data: dict[str, t.Any]):
        return super().test_update(
            f"/v1/personal/{ident}",
            self.__update_shema__.model_validate(data)
        )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("personals")
    def test_delete(self, index: int, personals: list[PersonalDTO]):
        personal = personals[index]

        return super().test_delete(
            "/v1/personal",
            self.__create_shema__.model_validate(personal.__dict__)
        )


class TestPersonalCertificationCRUDEndpoints(BaseTestCRUDEndpoints):
    __update_shema__ = UpdatePersonalNaksCertificationShema
    __create_shema__ = CreatePersonalNaksCertificationShema
    __dto__ = PersonalNaksCertificationDTO


    @pytest.mark.usefixtures("personal_certifications")
    def test_add(self, personal_certifications: list[PersonalNaksCertificationDTO]): 
        for certification in personal_certifications:
            super().test_add(
                "/v1/personal-naks-certification",
                self.__create_shema__.model_validate(certification.__dict__)
            )
        

    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("personal_certifications")
    def test_get(self, index: int, personal_certifications: list[PersonalNaksCertificationDTO]): 

        certification = personal_certifications[index]

        return super().test_get(
            f"/v1/personal-naks-certification/{certification.ident.hex}",
            certification
        )
        

    @pytest.mark.parametrize('execution_number', range(5))
    def test_get_certain_personal_certs(self, execution_number): 

        random_personal_ident = test_data.faker.random_element(test_data.fake_personal_certifications).personal_ident

        certifications = [cert for cert in test_data.fake_personal_certifications if cert.personal_ident == random_personal_ident]

        res = client.get(f"/v1/personal-naks-certification/personal/{random_personal_ident.hex}")
        
        assert len(certifications) == len(json.loads(res.text))


    @pytest.mark.parametrize(
        "ident, data",
        [(personal_certification.ident, new_personal_certification_data) for personal_certification, new_personal_certification_data in zip(test_data.fake_personal_certifications[:5], test_data.fake_personal_certification_generator.generate(5))]
    )
    def test_update(self, ident: str, data: dict[str, t.Any]):
        return super().test_update(
            f"/v1/personal-naks-certification/{ident}",
            self.__update_shema__.model_validate(data)
        )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("personal_certifications")
    def test_delete(self, index: int, personal_certifications: list[PersonalNaksCertificationDTO]):
        certification = personal_certifications[index]

        return super().test_delete(
            "/v1/personal-naks-certification",
            self.__create_shema__.model_validate(certification.__dict__)
        )


class TestNDTCRUDEndpoints(BaseTestCRUDEndpoints):
    __update_shema__ = UpdateNdtShema
    __create_shema__ = CreateNdtShema
    __dto__ = NdtDTO


    @pytest.mark.usefixtures("ndts")
    def test_add(self, ndts: list[NdtDTO]):

        for ndt in ndts:

            super().test_add(
                "/v1/ndt",
                self.__create_shema__.model_validate(ndt.__dict__)
            )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("ndts")
    def test_get(self, index: int, ndts: list[NdtDTO]):
        ndt = ndts[index]

        return super().test_get(
            f"/v1/ndt/{ndt.ident.hex}",
            ndt
        )
        

    @pytest.mark.parametrize('execution_number', range(5))
    def test_get_certain_personal_ndts(self, execution_number): 

        random_personal_ident = test_data.faker.random_element(test_data.fake_ndts).personal_ident

        ndts = [ndt for ndt in test_data.fake_ndts if ndt.personal_ident == random_personal_ident]

        res = client.get(f"/v1/ndt/personal/{random_personal_ident.hex}")
        
        assert len(ndts) == len(json.loads(res.text))


    @pytest.mark.parametrize(
        "ident, data",
        [(ndt.ident, new_ndt_data) for ndt, new_ndt_data in zip(test_data.fake_ndts[:5], test_data.fake_ndt_generator.generate(5))]
    )
    def test_update(self, ident: str, data: dict[str, t.Any]):
        return super().test_update(
            f"/v1/ndt/{ident}",
            self.__update_shema__.model_validate(data)
        )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("ndts")
    def test_delete(self, index: int, ndts: list[NdtDTO]):
        ndt = ndts[index]

        return super().test_delete(
            "/v1/ndt",
            self.__create_shema__.model_validate(ndt.__dict__)
        )
