import asyncio
import contextlib
import signal

from pycrdt_flow.backend.config import Config
from pycrdt_flow.backend.dbutils import open_db_session
from pycrdt_flow.backend.manager import RoomManager
from pycrdt_flow.backend.rds import open_redis_client
from pycrdt_flow.log import logger


async def event_wait(evt, timeout):
    # suppress TimeoutError because we'll return False in case of timeout
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(evt.wait(), timeout)
    return evt.is_set()


class DaemonMixin:
    interval = 0.1

    def __init__(self) -> None:
        self._stop_event = asyncio.Event()
        self._task: None | asyncio.Task = None

    async def initialize(self):
        pass

    async def run(self):
        pass

    async def cleanup(self):
        pass

    async def _start(self):
        if self._task is not None:
            raise RuntimeError("Already running")

        self._stop_event.clear()
        self._task = asyncio.create_task(self._task_wrapper())

    async def _stop(self):
        self._stop_event.set()
        if self._task is not None:
            logger.info("Waiting for task to finish...")
            await self._task

    async def _task_wrapper(self):
        try:
            await self.initialize()
        except Exception as e:
            # Unexpected error, stop the autoscaler
            logger.exception(e)
            exit(1)

        await self.run()
        while not await event_wait(self._stop_event, self.interval):
            if self._stop_event.is_set():
                break
            try:
                await self.run()
            except Exception as e:
                logger.exception(e)

        await self.cleanup()

    async def run_forever(self, stop_signals: list = [signal.SIGINT, signal.SIGTERM]):
        loop = asyncio.get_event_loop()

        stop_event = asyncio.Event()

        async def _stop():
            logger.debug("Signal received")
            stop_event.set()

        for sig in stop_signals:
            loop.add_signal_handler(sig, lambda: asyncio.create_task(_stop()))

        logger.info(f"Starting daemon...")
        await self._start()
        logger.info(f"Daemon started, waiting for signals {stop_signals}...")
        await stop_event.wait()

        logger.info(f"Terminating daemon...")
        await self._stop()
        logger.info(f"Daemon terminated")


class RoomPersistenceDaemon(DaemonMixin):
    interval = 60

    def __init__(self, config: Config) -> None:
        super().__init__()
        self.config = config

    async def run(self):
        logger.debug("Persisting rooms...")
        async with open_redis_client(self.config) as redis_client:
            async with open_db_session(self.config) as session:
                await RoomManager(session=session, redis_client=redis_client).persist_all()
