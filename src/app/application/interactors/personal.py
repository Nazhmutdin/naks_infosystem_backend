from naks_library.interactors import BaseCreateInteractor, BaseGetInteractor, BaseUpdateInteractor, BaseDeleteInteractor, BaseSelectInteractor

from app.application.dto import PersonalDTO, CreatePersonalDTO


class CreatePersonalInteractor(BaseCreateInteractor[CreatePersonalDTO]): ...


class GetPersonalInteractor(BaseGetInteractor[PersonalDTO]): ...


class SelectPersonalInteractor(BaseSelectInteractor[PersonalDTO]): ...


class UpdatePersonalInteractor(BaseUpdateInteractor): ...


class DeletePersonalInteractor(BaseDeleteInteractor): ...
