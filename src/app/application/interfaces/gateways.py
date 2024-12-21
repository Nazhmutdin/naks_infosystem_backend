from uuid import UUID

from naks_library.interfaces import ICrudGateway

from app.application.dto import (
    PersonalDTO,
    CreatePersonalDTO,
    PersonalNaksCertificationDTO,
    CreatePersonalNaksCertificationDTO,
    NdtDTO, 
    CreateNdtDTO,
    AcstDTO,
    CreateAcstDTO
)


class PersonalGateway(ICrudGateway[PersonalDTO, CreatePersonalDTO]): ...


class PersonalNaksCertificationGateway(ICrudGateway[PersonalNaksCertificationDTO, CreatePersonalNaksCertificationDTO]):

    async def get_certain_personal_naks_certifications(self, personal_ident: UUID) -> list[PersonalNaksCertificationDTO]: ...

    async def get_personal_naks_certification_html(self, ident: UUID) -> str | None: ...


class NdtGateway(ICrudGateway[NdtDTO, CreateNdtDTO]):

    async def get_certain_personal_ndts(self, personal_ident: UUID) -> list[NdtDTO]: ...


class AcstGateway(ICrudGateway[AcstDTO, CreateAcstDTO]):
    async def get_acst_html(self, ident: UUID) -> str | None: ...
