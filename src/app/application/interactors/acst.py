from naks_library.interactors import BaseCreateInteractor, BaseGetInteractor, BaseUpdateInteractor, BaseDeleteInteractor, BaseSelectInteractor

from app.application.dto import AcstDTO, CreateAcstDTO, UpdateAcstDTO


class CreateAcstInteractor(BaseCreateInteractor[CreateAcstDTO]): ...


class GetAcstInteractor(BaseGetInteractor[AcstDTO]): ...


class SelectAcstInteractor(BaseSelectInteractor[AcstDTO]): ...


class UpdateAcstInteractor(BaseUpdateInteractor[UpdateAcstDTO]): ...


class DeleteAcstInteractor(BaseDeleteInteractor): ...
