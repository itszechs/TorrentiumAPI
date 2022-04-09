import asyncio
import uuid
from typing import Any, List

import aiohttp

import src.modules.aria.utils as utils
from src.modules.aria.method import Method
from src.modules.aria.model import AriaStats


class Aria2c:
    def __init__(
            self,
            host: str = "http://localhost",
            port: int = 6800,
            secret: str = None
    ):
        host = host.rstrip("/")

        self.host = host
        self.port = port
        self.secret = secret
        self.client = aiohttp.ClientSession()

    def __del__(self):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.client.close())
            else:
                loop.run_until_complete(self.client.close())
        except Exception:
            pass

    def __repr__(self):
        return f"<Aria2c host={self.host} port={self.port}>"

    async def __post(
            self,
            method: Method,
            params: List[Any] = None
    ) -> dict:
        url = f"{self.host}:{self.port}/jsonrpc"

        if params is None:
            params = []

        if self.secret:
            params.insert(0, f"token:{self.secret}")

        data = {
            "id": str(uuid.uuid4()),
            "jsonrpc": "2.0",
            "method": method.value,
            "params": params
        }

        async with self.client.post(
                url,
                json=data,
                headers={"Content-Type": "application/json"}
        ) as r:
            return await r.json()

    async def add_uri(
            self,
            uris: List[str],
            options: dict = None
    ) -> dict:
        if uris is None:
            raise ValueError("uris is required")

        params = []
        params.insert(0, uris)

        if options is not None:
            params.insert(1, options)

        return await self.__post(Method.ADD_URI, params)

    async def get_version(self) -> str:
        res = await self.__post(Method.GET_VERSION)
        version = res['result']['version']
        return version

    async def resume(
            self, gid
    ) -> dict:
        return await self.__post(Method.UNPAUSE, params=[gid])

    async def pause(
            self, gid
    ) -> dict:
        return await self.__post(Method.PAUSE, params=[gid])

    async def remove(
            self, gid
    ) -> dict:
        return await self.__post(Method.REMOVE, params=[gid])

    async def __tell_active(self):
        return await self.__post(Method.TELL_ACTIVE)

    async def __tell_waiting(self):
        return await self.__post(Method.TELL_WAITING, params=[0, 1000])

    async def __tell_stopped(self):
        return await self.__post(Method.TELL_STOPPED, params=[0, 1000])

    async def get_download(
            self, gid
    ) -> dict:
        return await self.__post(Method.TELL_STATUS, params=[gid])

    async def get_downloads(self) -> List[dict]:
        await self.purge_download_result()
        try:
            active = await self.__tell_active()
            waiting = await self.__tell_waiting()
            stopped = await self.__tell_stopped()
            downloads = []
            downloads.extend(active['result'])
            downloads.extend(waiting['result'])
            downloads.extend(stopped['result'])
            return utils.parse_downloads(downloads)
        except KeyError:
            return []

    async def purge_download_result(self) -> dict:
        return await self.__post(Method.PURGE_DOWNLOAD_RESULT)

    async def get_global_stat(self) -> AriaStats:
        res = await self.__post(Method.GET_GLOBAL_STAT)
        result = res['result']
        return AriaStats(
            num_active=int(result['numActive']),
            num_stopped=int(result['numStopped']),
            num_waiting=int(result['numWaiting'])
        )
