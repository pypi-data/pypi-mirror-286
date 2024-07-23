from fastapi import Cookie, Depends, Query, WebSocket, WebSocketException, status
from jose import JWSError

from pycrdt_flow.backend.config import Config, get_config
from pycrdt_flow.log import logger
from pycrdt_flow.permission import COOKIE_NAME, TOKEN_NAME, Permissions


async def get_cookie_or_token(
    websocket: WebSocket,
    config: Config = Depends(get_config),
    session: str | None = Cookie(default=None, alias=COOKIE_NAME),
    token: str | None = Query(default=None, alias=TOKEN_NAME),
):
    if not config.jwt_secret:
        return ""
    if session is None and token is None:
        logger.debug("Neither session nor token provided")
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


def get_current_permission(
    websocket: WebSocket,
    config: Config = Depends(get_config),
    cookie_or_token: str = Depends(get_cookie_or_token),
) -> Permissions:
    if not config.jwt_secret:
        return Permissions.all_permissions()

    try:
        return Permissions.from_token(config.jwt_secret, cookie_or_token)
    except JWSError:
        logger.debug(f"Invalid token provided: {cookie_or_token}")
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
