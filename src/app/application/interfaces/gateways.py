from uuid import UUID

from naks_library.interfaces import ICrudGateway

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


class PersonalGateway(ICrudGateway[PersonalDTO, CreatePersonalDTO, UpdatePersonalDTO]): ...


class PersonalNaksCertificationGateway(ICrudGateway[PersonalNaksCertificationDTO, CreatePersonalNaksCertificationDTO, UpdatePersonalNaksCertificationDTO]):

    async def get_certain_personal_naks_certifications(self, personal_ident: UUID) -> list[PersonalNaksCertificationDTO]: ...


class NdtGateway(ICrudGateway[NdtDTO, CreateNdtDTO, UpdateNdtDTO]):

    async def get_certain_personal_ndts(self, personal_ident: UUID) -> list[NdtDTO]: ...


class AcstGateway(ICrudGateway[AcstDTO, CreateAcstDTO, UpdateAcstDTO]): ...
