from pydantic import BaseModel


class AuthData(BaseModel):
    password: str
    login: str