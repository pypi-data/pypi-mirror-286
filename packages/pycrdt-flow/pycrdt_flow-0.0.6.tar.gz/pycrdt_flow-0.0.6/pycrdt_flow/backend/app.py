import os
from contextlib import asynccontextmanager

import starlette
from fastapi import Depends, FastAPI, WebSocket, WebSocketException

from pycrdt_flow.backend.auth import get_current_permission
from pycrdt_flow.backend.config import get_config
from pycrdt_flow.backend.envs import JWT_SECRET_ENV
from pycrdt_flow.backend.manager import RoomManager, get_room_manager
from pycrdt_flow.log import logger
from pycrdt_flow.permission import Permissions


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = get_config()
    if not os.getenv(JWT_SECRET_ENV):
        logger.info(f"Random generated jwt secret is {config.jwt_secret}")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.websocket("/ws/{room_id}/room")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    permission: Permissions = Depends(get_current_permission),
    room_manager: RoomManager = Depends(get_room_manager),
):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}, permission: {permission}")
        except starlette.websockets.WebSocketDisconnect as e:
            if e.code == 1000:
                break
            raise


@app.websocket("/ws/{room_id}/awareness")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    permission: Permissions = Depends(get_current_permission),
    awareness_manager: RoomManager = Depends(get_room_manager),
):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}, permission: {permission}")
        except starlette.websockets.WebSocketDisconnect as e:
            if e.code == 1000:
                break
            raise
