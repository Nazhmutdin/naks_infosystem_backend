from uuid import UUID


class PersonalNotFoundException(Exception):
    def __init__(self, ident: UUID) -> None:
        self.ident = ident


class PersonalNaksCertificationNotFoundException(Exception):
    def __init__(self, ident: UUID) -> None:
        self.ident = ident


class NdtNotFoundException(Exception):
    def __init__(self, ident: UUID) -> None:
        self.ident = ident
