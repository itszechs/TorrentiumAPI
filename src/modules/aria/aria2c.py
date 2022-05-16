import json
import shutil
import uuid
from pathlib import Path
from typing import Any, List, Dict

import requests

import src.modules.aria.utils as utils
from src.modules.aria.method import Method
from src.modules.aria.model import AriaStats


def remove_files(download) -> None:
    try:
        files = download['result']['files']
        _dir = Path(download['result']['dir'])
        for file in files:
            if file['path'].startswith("[METADATA]"):
                continue
            try:
                relative_path = Path(file['path']).relative_to(_dir)
            except ValueError:
                print(f"Can't determine file path '{file['path']}' relative to '{_dir}'")
            else:
                path = _dir / relative_path.parts[0]
                if path.is_dir():
                    try:
                        shutil.rmtree(str(path))
                    except OSError:
                        print(f"Could not delete directory '{path}'")
                else:
                    try:
                        path.unlink()
                    except FileNotFoundError:
                        print(f"File '{path}' did not exist when trying to delete it")
    except KeyError:
        pass


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
        self.__session = requests.Session()

    def __repr__(self):
        return f"<Aria2c host={self.host} port={self.port}>"

    def __post(
            self,
            method: Method,
            params: List[Any] = None
    ) -> Dict:
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

        with self.__session.post(
                url,
                data=json.dumps(data),
                headers={"Content-Type": "application/json"}
        ) as r:
            return r.json()

    def add_uri(
            self,
            uris: List[str],
            options: Dict = None
    ) -> Dict:
        if uris is None:
            raise ValueError("uris is required")

        params = []
        params.insert(0, uris)

        if options is not None:
            params.insert(1, options)

        return self.__post(Method.ADD_URI, params)

    def get_version(self) -> str:
        res = self.__post(Method.GET_VERSION)
        version = res['result']['version']
        return version

    def resume(
            self, gid
    ) -> Dict:
        return self.__post(Method.UNPAUSE, params=[gid])

    def pause(
            self, gid
    ) -> Dict:
        return self.__post(Method.PAUSE, params=[gid])

    def remove(
            self, gid, files=False
    ) -> Dict:
        if files:
            download = self.get_download(gid)
            remove_files(download)
        return self.__post(Method.REMOVE, params=[gid])

    def __tell_active(self):
        return self.__post(Method.TELL_ACTIVE)

    def __tell_waiting(self):
        return self.__post(Method.TELL_WAITING, params=[0, 1000])

    def __tell_stopped(self):
        return self.__post(Method.TELL_STOPPED, params=[0, 1000])

    def get_download(
            self, gid
    ) -> Dict:
        return self.__post(Method.TELL_STATUS, params=[gid])

    def get_downloads(self) -> List[Dict]:
        self.purge_download_result()

        try:
            active = self.__tell_active()
            waiting = self.__tell_waiting()
            stopped = self.__tell_stopped()
            downloads = []
            downloads.extend(active['result'])
            downloads.extend(waiting['result'])
            downloads.extend(stopped['result'])
            return utils.parse_downloads(downloads)
        except KeyError:
            return []

    def purge_download_result(self) -> Dict:
        return self.__post(Method.PURGE_DOWNLOAD_RESULT)

    def get_global_stat(self) -> AriaStats:
        res = self.__post(Method.GET_GLOBAL_STAT)
        result = res['result']
        return AriaStats(
            num_active=int(result['numActive']),
            num_stopped=int(result['numStopped']),
            num_waiting=int(result['numWaiting'])
        )
