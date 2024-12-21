from uuid import UUID
from naks_library.interactors import BaseCreateInteractor, BaseGetInteractor, BaseUpdateInteractor, BaseDeleteInteractor, BaseSelectInteractor

from app.application.dto import AcstDTO, CreateAcstDTO
from app.application.interfaces.gateways import AcstGateway


class CreateAcstInteractor(BaseCreateInteractor[CreateAcstDTO]): ...


class GetAcstInteractor(BaseGetInteractor[AcstDTO]): ...


class GetAcstHtmlInteractor:
    def __init__(
        self,
        gateway: AcstGateway
    ) -> None:
        self.gateway = gateway

    
    async def __call__(self, ident: UUID) -> str | None:
        return await self.gateway.get_acst_html(ident)


class SelectAcstInteractor(BaseSelectInteractor[AcstDTO]): ...


class UpdateAcstInteractor(BaseUpdateInteractor): ...


class DeleteAcstInteractor(BaseDeleteInteractor): ...
