import pytest

from pycrdt_flow.backend.config import get_config
from pycrdt_flow.permission import PermissionEnum, Permissions


@pytest.fixture
def jwt_secret():
    return get_config().jwt_secret


@pytest.mark.parametrize(
    "permissions",
    [
        [],
        [PermissionEnum.READ],
        [PermissionEnum.WRITE],
        [PermissionEnum.READ, PermissionEnum.WRITE],
    ],
)
def test_permissions(jwt_secret, permissions):
    p = Permissions(permissions=permissions)

    if PermissionEnum.READ in permissions:
        assert p.is_readable()
    else:
        assert not p.is_readable()

    if PermissionEnum.WRITE in permissions:
        assert p.is_writable()
    else:
        assert not p.is_writable()

    token = p.sign_token(jwt_secret)
    p_from_token = Permissions.from_token(jwt_secret, token)

    assert p == p_from_token
