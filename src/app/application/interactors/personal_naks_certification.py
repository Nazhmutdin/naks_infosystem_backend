from naks_library.interactors import BaseCreateInteractor, BaseGetInteractor, BaseUpdateInteractor, BaseDeleteInteractor, BaseSelectInteractor

from app.application.dto import PersonalNaksCertificationDTO, CreatePersonalNaksCertificationDTO, UpdatePersonalNaksCertificationDTO


class CreatePersonalNaksCertificationInteractor(BaseCreateInteractor[CreatePersonalNaksCertificationDTO]): ...


class GetPersonalNaksCertificationInteractor(BaseGetInteractor[PersonalNaksCertificationDTO]): ...


class SelectPersonalNaksCertificationInteractor(BaseSelectInteractor[PersonalNaksCertificationDTO]): ...


class UpdatePersonalNaksCertificationInteractor(BaseUpdateInteractor[UpdatePersonalNaksCertificationDTO]): ...


class DeletePersonalNaksCertificationInteractor(BaseDeleteInteractor): ...
