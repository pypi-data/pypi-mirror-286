from __future__ import annotations

import enum

from jose import jws
from pydantic import BaseModel

TOKEN_NAME = "pycrdt-flow-token"
COOKIE_NAME = "pycrdt-flow-session"


def sign_token(obj: dict, secret_key: str) -> str:
    return jws.sign(obj, secret_key, algorithm="HS256")


def verify_token(token: str, secret_key: str) -> str:
    return jws.verify(token, secret_key, algorithms="HS256").decode()


class PermissionEnum(str, enum.Enum):
    READ = "read"
    WRITE = "write"


class Permissions(BaseModel):
    permissions: list[PermissionEnum]

    def is_readable(self) -> bool:
        return PermissionEnum.READ in self.permissions

    def is_writable(self) -> bool:
        return PermissionEnum.WRITE in self.permissions

    def sign_token(self, jwt_secret: str) -> str:
        return sign_token(self.model_dump(mode="json"), jwt_secret)

    @classmethod
    def from_token(cls, jwt_secret: str, token: str) -> "Permissions":
        return cls.model_validate_json(verify_token(token, jwt_secret))

    @classmethod
    def all_permissions(cls) -> "Permissions":
        return cls(permissions=[PermissionEnum.READ, PermissionEnum.WRITE])
