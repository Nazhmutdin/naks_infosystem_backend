from uuid import UUID
from naks_library.interactors import BaseCreateInteractor, BaseGetInteractor, BaseUpdateInteractor, BaseDeleteInteractor, BaseSelectInteractor

from app.application.dto import PersonalNaksCertificationDTO, CreatePersonalNaksCertificationDTO
from app.application.interfaces.gateways import PersonalNaksCertificationGateway


class CreatePersonalNaksCertificationInteractor(BaseCreateInteractor[CreatePersonalNaksCertificationDTO]): ...


class GetPersonalNaksCertificationInteractor(BaseGetInteractor[PersonalNaksCertificationDTO]): ...


class GetCertainPersonalNaksCertificationsInteractor:
    def __init__(
        self,
        gateway: PersonalNaksCertificationGateway
    ) -> None:
        self.gateway = gateway

    
    async def __call__(self, personal_ident: UUID) -> list[PersonalNaksCertificationDTO]:
        return await self.gateway.get_certain_personal_naks_certifications(personal_ident)


class GetPersonalNaksCertificationHtmlInteractor:
    def __init__(
        self,
        gateway: PersonalNaksCertificationGateway
    ) -> None:
        self.gateway = gateway

    
    async def __call__(self, ident: UUID) -> str | None:
        return await self.gateway.get_personal_naks_certification_html(ident)


class SelectPersonalNaksCertificationInteractor(BaseSelectInteractor[PersonalNaksCertificationDTO]): ...


class UpdatePersonalNaksCertificationInteractor(BaseUpdateInteractor): ...


class DeletePersonalNaksCertificationInteractor(BaseDeleteInteractor): ...
