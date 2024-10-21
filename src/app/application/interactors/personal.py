from naks_library.interactors import BaseCreateInteractor, BaseGetInteractor, BaseUpdateInteractor, BaseDeleteInteractor, BaseSelectInteractor

from app.application.dto import PersonalDTO, CreatePersonalDTO, UpdatePersonalDTO


class CreatePersonalInteractor(BaseCreateInteractor[CreatePersonalDTO]): ...


class GetPersonalInteractor(BaseGetInteractor[PersonalDTO]): ...


class SelectPersonalInteractor(BaseSelectInteractor[PersonalDTO]): ...


class UpdatePersonalInteractor(BaseUpdateInteractor[UpdatePersonalDTO]): ...


class DeletePersonalInteractor(BaseDeleteInteractor): ...
