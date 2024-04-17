import typing as t
from uuid import UUID
from datetime import datetime
from hashlib import sha256

from jose.jwt import encode as jwt_encode, decode as jwt_decode

from settings import Settings


class AccessTokenPayloadData(t.TypedDict):
    exp_dt: datetime
    user_id: UUID


class RefreshTokenPayloadData(t.TypedDict):
    gen_dt: datetime
    exp_dt: datetime
    user_id: UUID


class AuthService:
    def __init__(self, alg: str | list[str]="HS256") -> None:
        self.algorithms = alg


    def create_token(self, **payloads: t.Unpack[AccessTokenPayloadData]) -> str:

        if not payloads.get("exp_dt"):
            raise ValueError("exp_dt is required")

        if not payloads.get("user_id"):
            raise ValueError("user_id is required")

        if not isinstance(payloads.get("exp_dt"), datetime):
            raise ValueError("exp_dt must be datetime object")

        if not isinstance(payloads.get("user_id"), UUID):
            try:
                payloads["user_id"] = UUID(payloads["user_id"])
            except:
                raise ValueError("invalid user_id")
        
        payloads["exp_dt"] = payloads["exp_dt"].strftime("%Y/%m/%d, %H:%M:%S")
        payloads["user_id"] = payloads["user_id"].hex

        return jwt_encode(payloads, Settings.SECRET_KEY(), algorithm=self.algorithms)


    def gen_refresh_token(self, **payloads: t.Unpack[RefreshTokenPayloadData]):

        if not payloads.get("gen_dt"):
            raise ValueError("gen is required")

        if not payloads.get("exp_dt"):
            raise ValueError("exp_dt is required")

        if not payloads.get("user_id"):
            raise ValueError("user_id is required")

        if not isinstance(payloads.get("exp_dt"), datetime):
            raise ValueError("exp_dt must be datetime object")

        if not isinstance(payloads.get("gen_dt"), datetime):
            raise ValueError("gen_dt must be datetime object")

        if not isinstance(payloads.get("user_id"), UUID):
            try:
                payloads["user_id"] = UUID(payloads["user_id"])
            except:
                raise ValueError("invalid user_id")
        
        payloads["gen_dt"] = payloads["gen_dt"].strftime("%Y/%m/%d, %H:%M:%S")
        
        payloads["exp_dt"] = payloads["exp_dt"].strftime("%Y/%m/%d, %H:%M:%S")
        payloads["user_id"] = payloads["user_id"].hex

        return jwt_encode(payloads, Settings.SECRET_KEY(), algorithm=self.algorithms)


    def read_token(self, token: str) -> dict[str, t.Any]:
        return jwt_decode(token, Settings.SECRET_KEY(), algorithms=self.algorithms)


    def hash_password(self, password: str) -> str:
        return sha256(password.encode()).hexdigest()


    def validate_password(self, password: str, hashed_password: str) -> bool:
        return sha256(password.encode()).hexdigest() == hashed_password
