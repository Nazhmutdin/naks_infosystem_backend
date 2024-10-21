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
    UpdateNdtDTO
)


class PersonalGateway(ICrudGateway[PersonalDTO, CreatePersonalDTO, UpdatePersonalDTO]): ...


class PersonalNaksCertificationGateway(ICrudGateway[PersonalNaksCertificationDTO, CreatePersonalNaksCertificationDTO, UpdatePersonalNaksCertificationDTO]): ...


class NdtGateway(ICrudGateway[NdtDTO, CreateNdtDTO, UpdateNdtDTO]): ...
