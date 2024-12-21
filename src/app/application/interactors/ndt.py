from uuid import UUID
from naks_library.interactors import BaseCreateInteractor, BaseGetInteractor, BaseUpdateInteractor, BaseDeleteInteractor, BaseSelectInteractor

from app.application.dto import NdtDTO, CreateNdtDTO
from app.application.interfaces.gateways import NdtGateway


class CreateNdtInteractor(BaseCreateInteractor[CreateNdtDTO]): ...


class GetNdtInteractor(BaseGetInteractor[NdtDTO]): ...


class GetCertainPersonalNdtsInteractor:
    def __init__(
        self,
        gateway: NdtGateway
    ) -> None:
        self.gateway = gateway

    
    async def __call__(self, personal_ident: UUID) -> list[NdtDTO]:
        return await self.gateway.get_certain_personal_ndts(personal_ident)


class SelectNdtInteractor(BaseSelectInteractor[NdtDTO]): ...


class UpdateNdtInteractor(BaseUpdateInteractor): ...


class DeleteNdtInteractor(BaseDeleteInteractor): ...
