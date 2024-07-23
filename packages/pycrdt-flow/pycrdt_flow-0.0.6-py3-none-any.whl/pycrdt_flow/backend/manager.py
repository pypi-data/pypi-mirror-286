from __future__ import annotations

from typing import Awaitable

import redis.asyncio as redis
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from pycrdt_flow.backend.dbutils import get_db_session
from pycrdt_flow.backend.rds import get_redis_client
from pycrdt_flow.log import logger


class RedisMixin:
    separator = ":"
    prefix = "pycrdt-flow"
    redis_client: redis.Redis | redis.RedisCluster

    def get_room_key(self, room_id: str) -> str:
        return self.separator.join(
            [
                self.prefix,
                "room",
                "{%s}" % room_id,
            ]
        )

    def get_awareness_key(self, room_id: str) -> str:
        return self.separator.join(
            [
                self.prefix,
                "awareness",
                "{%s}" % room_id,
            ]
        )

    async def scan_rooms(self, async_callback: Awaitable[str]) -> None:
        async for key in self.redis_client.scan_iter(
            self.separator.join([self.prefix, "room", "*"])
        ):
            await async_callback(key)


def get_awareness_manager(
    redis_client: redis.Redis | redis.RedisCluster = Depends(get_redis_client),
) -> AwarenessManager:
    return AwarenessManager(redis_client=redis_client)


class AwarenessManager(RedisMixin):
    def __init__(self, redis_client: redis.Redis) -> None:
        self.redis_client = redis_client


def get_room_manager(
    session: AsyncSession = Depends(get_db_session),
    redis_client: redis.Redis | redis.RedisCluster = Depends(get_redis_client),
) -> RoomManager:
    return RoomManager(session=session, redis_client=redis_client)


class RoomManager(RedisMixin):
    def __init__(self, session: AsyncSession, redis_client: redis.Redis) -> None:
        self.session = session
        self.redis_client = redis_client

    async def persist_all(self) -> None:
        await self.scan_rooms(self.presist_room)

    async def presist_room(self, room_id: str) -> None:
        logger.debug("Persisting room: %s", room_id)
