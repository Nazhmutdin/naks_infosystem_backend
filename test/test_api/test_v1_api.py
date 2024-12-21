import typing as t
from uuid import UUID
import json

import pytest
from client import client
from pydantic import RootModel

from app.application.dto import (
    PersonalDTO, 
    CreatePersonalDTO,
    UpdatePersonalDTO,
    PersonalNaksCertificationDTO, 
    CreatePersonalNaksCertificationDTO, 
    UpdatePersonalNaksCertificationDTO,
    NdtDTO, 
    CreateNdtDTO, 
    UpdateNdtDTO,
    AcstDTO, 
    CreateAcstDTO,
    UpdateAcstDTO
)
from funcs import test_data


class BaseTestCRUDEndpoints[DTO, CreateDTO]:
    __dto__: type[DTO]
    __create_dto__: type[CreateDTO]


    def test_add(self, api_path, item: DTO):
        res = client.post(
            api_path, 
            json=RootModel[CreateDTO](item).model_dump(mode="json")
        )

        assert res.status_code == 200


    def test_get(self, api_path: str, ident: UUID, item: DTO):
        res = client.get(api_path, params={"ident": ident.hex})

        sub_data = json.loads(res.text)

        assert item == self.__dto__(**sub_data)


    def test_update(self, api_path: str, ident: UUID, data: RootModel):
        res = client.patch(
            api_path, 
            params={"ident": ident.hex},
            json=data.model_dump(mode="json")
        )

        assert res.status_code == 200

        res = client.get(api_path, params={"ident": ident.hex})

        assert res.status_code == 200

        result: dict = data.model_validate(json.loads(res.text)).model_dump(mode="json", by_alias=False)

        for key, value in data.model_dump(mode="json", by_alias=False).items():
            assert result[key] == value


    def test_delete(self, api_path: str, ident: UUID, item: DTO): 
        res = client.delete(api_path, params={"ident": ident.hex})

        assert res.status_code == 200

        assert client.get(api_path, params={"ident": ident.hex}).status_code == 404
        
        res = client.post(
            api_path, 
            json=RootModel[CreateDTO](item).model_dump(mode="json")
        )

        assert res.status_code == 200


class TestPersonalCRUDEndpoints(BaseTestCRUDEndpoints[PersonalDTO, CreatePersonalDTO]):
    __create_dto__ = CreatePersonalDTO
    __dto__ = PersonalDTO


    def test_add(self):
        for personal in test_data.fake_personals_dicts:

            super().test_add(
                "/v1/personal",
                self.__create_dto__(**personal)
            )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("personals")
    def test_get(self, index: int, personals: list[PersonalDTO]):

        personal = personals[index]

        return super().test_get(
            "/v1/personal",
            personal.ident,
            personal
        )

    @pytest.mark.parametrize(
        "ident, data",
        [(personal.ident, new_personal_data) for personal, new_personal_data in zip(test_data.fake_personals[:5], test_data.fake_personal_generator.generate(5))]
    )
    def test_update(self, ident: str, data: dict[str, t.Any]):

        return super().test_update(
            "/v1/personal",
            ident,
            RootModel[UpdatePersonalDTO](data)
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
            personal.ident,
            self.__create_dto__(**personal.__dict__)
        )


class TestPersonalCertificationCRUDEndpoints(BaseTestCRUDEndpoints[PersonalNaksCertificationDTO, CreatePersonalNaksCertificationDTO]):
    __create_dto__ = CreatePersonalNaksCertificationDTO
    __dto__ = PersonalNaksCertificationDTO


    def test_add(self): 
        for certification in test_data.fake_personal_certifications_dicts:
            super().test_add(
                "/v1/personal-naks-certification",
                self.__create_dto__(**certification)
            )
        

    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("personal_certifications")
    def test_get(self, index: int, personal_certifications: list[PersonalNaksCertificationDTO]): 

        certification = personal_certifications[index]

        return super().test_get(
            "/v1/personal-naks-certification",
            certification.ident,
            certification
        )
        

    @pytest.mark.parametrize('execution_number', range(5))
    def test_get_certain_personal_certs(self, execution_number): 

        random_personal_ident = test_data.faker.random_element(test_data.fake_personal_certifications).personal_ident

        certifications = [cert for cert in test_data.fake_personal_certifications if cert.personal_ident == random_personal_ident]

        res = client.get(
            "/v1/personal-naks-certification/personal",
            params={
                "personal_ident": random_personal_ident.hex
            }
        )
        
        assert len(certifications) == len(json.loads(res.text))


    @pytest.mark.parametrize(
        "ident, data",
        [(personal_certification.ident, new_personal_certification_data) for personal_certification, new_personal_certification_data in zip(test_data.fake_personal_certifications[:5], test_data.fake_personal_certification_generator.generate(5))]
    )
    def test_update(self, ident: str, data: dict[str, t.Any]):

        return super().test_update(
            "/v1/personal-naks-certification",
            ident,
            RootModel[UpdatePersonalNaksCertificationDTO](data)
        )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("personal_certification_dicts")
    def test_delete(self, index: int, personal_certification_dicts: list[dict]):

        certification = personal_certification_dicts[index]

        return super().test_delete(
            "/v1/personal-naks-certification",
            certification["ident"],
            self.__create_dto__(**certification)
        )


class TestNDTCRUDEndpoints(BaseTestCRUDEndpoints[NdtDTO, CreateNdtDTO]):
    __update_dto__ = UpdateNdtDTO
    __create_dto__ = CreateNdtDTO
    __dto__ = NdtDTO


    def test_add(self):
        for ndt in test_data.fake_ndts_dicts:

            super().test_add(
                "/v1/ndt",
                self.__create_dto__(**ndt)
            )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("ndts")
    def test_get(self, index: int, ndts: list[NdtDTO]):
        ndt = ndts[index]

        return super().test_get(
            "/v1/ndt",
            ndt.ident,
            ndt
        )
        

    @pytest.mark.parametrize('execution_number', range(5))
    def test_get_certain_personal_ndts(self, execution_number): 

        random_personal_ident = test_data.faker.random_element(test_data.fake_ndts).personal_ident

        ndts = [ndt for ndt in test_data.fake_ndts if ndt.personal_ident == random_personal_ident]

        res = client.get(
            "/v1/ndt/personal",
            params={
                "personal_ident": random_personal_ident.hex
            }
        )
        
        assert len(ndts) == len(json.loads(res.text))


    @pytest.mark.parametrize(
        "ident, data",
        [(ndt.ident, new_ndt_data) for ndt, new_ndt_data in zip(test_data.fake_ndts[:5], test_data.fake_ndt_generator.generate(5))]
    )
    def test_update(self, ident: str, data: dict[str, t.Any]):
        return super().test_update(
            "/v1/ndt",
            ident,
            RootModel[UpdateNdtDTO](data)
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
            ndt.ident,
            self.__create_dto__(**ndt.__dict__)
        )


class TestAcstCRUDEndpoints(BaseTestCRUDEndpoints[AcstDTO, CreateAcstDTO]):
    __update_dto__ = UpdateAcstDTO
    __create_dto__ = CreateAcstDTO
    __dto__ = AcstDTO


    def test_add(self):

        for acst in test_data.fake_acsts_dicts:

            super().test_add(
                "/v1/acst",
                self.__create_dto__(**acst)
            )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("acsts")
    def test_get(self, index: int, acsts: list[AcstDTO]):
        acst = acsts[index]

        return super().test_get(
            "/v1/acst",
            acst.ident,
            acst
        )


    @pytest.mark.parametrize(
        "ident, data",
        [(acst.ident, new_acst_data) for acst, new_acst_data in zip(test_data.fake_acsts[:5], test_data.fake_acst_generator.generate(5))]
    )
    def test_update(self, ident: str, data: dict[str, t.Any]):
        return super().test_update(
            "/v1/acst",
            ident,
            RootModel[UpdateAcstDTO](data)
        )


    @pytest.mark.parametrize(
            "index",
            [0, 1, 2, 3]
    )
    @pytest.mark.usefixtures("acst_dicts")
    def test_delete(self, index: int, acst_dicts: list[dict]):
        acst = acst_dicts[index]

        return super().test_delete(
            "/v1/acst",
            acst["ident"],
            self.__create_dto__(**acst)
        )
