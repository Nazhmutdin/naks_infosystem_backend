from naks_library.interactors import BaseCreateInteractor, BaseGetInteractor, BaseUpdateInteractor, BaseDeleteInteractor, BaseSelectInteractor

from app.application.dto import NdtDTO, CreateNdtDTO, UpdateNdtDTO


class CreateNdtInteractor(BaseCreateInteractor[CreateNdtDTO]): ...


class GetNdtInteractor(BaseGetInteractor[NdtDTO]): ...


class SelectNdtInteractor(BaseSelectInteractor[NdtDTO]): ...


class UpdateNdtInteractor(BaseUpdateInteractor[UpdateNdtDTO]): ...


class DeleteNdtInteractor(BaseDeleteInteractor): ...
