from typing import Dict
from typing import Optional, List

import requests

from src.modules.rclone.method import Method, Operation
from src.modules.rclone.model import Version, Remotes, \
    JobsList, CoreStats, Transfer
from src.modules.rclone.utils import split_path


class RcloneRC:

    def __init__(
            self,
            host: str = "http://localhost",
            port: Optional[int] = 5572
    ):
        host = host.rstrip("/")

        self.host = host
        self.port = port

        self.__session = requests.Session()

    def __post(self, method: Method, params: Dict = None):
        url = self.host

        if self.port is not None:
            url += f":{self.port}"

        url += f"/{method.value}"

        if params is None:
            params = {}

        return self.__session.post(url, data=params).json()

    def get_version(self) -> Version:
        version = self.__post(Method.CORE_VERSION)
        return Version.from_dict(version)

    def list_remotes(self) -> Remotes:
        remotes = self.__post(Method.LIST_REMOTES)
        return Remotes.from_dict(remotes)

    def get_jobs(self) -> JobsList:
        jobs_list = self.__post(Method.JOB_LIST)
        return JobsList.from_dict(jobs_list)

    def stop_job(self, job_id: int) -> None:
        self.__post(Method.JOB_STOP, {"jobid": job_id})

    def __operation(
            self,
            operation: Operation,
            source: str,
            destination: str,
            createEmptySrcDirs: bool = False,
            deleteEmptySrcDirs: bool = False
    ) -> str:
        source_remote, source_path = split_path(source)
        destination_remote, destination_path = split_path(destination)

        fsinfo = self.__post(
            Method.OPERATIONS_LIST,
            {
                "fs": source_remote,
                "remote": source_path
            }
        )

        try:
            if fsinfo['status'] == 500:
                if "not a directory" in fsinfo['error']:
                    is_file = True
                    path_exists = True
                else:
                    is_file = False
                    path_exists = False
            else:
                is_file = False
                path_exists = False
        except KeyError:
            is_file = False
            path_exists = True

        if not path_exists:
            return "Source path does not exist"

        if is_file:
            params = {
                "srcFs": source_remote,
                "srcRemote": source_path,
                "dstFs": destination_remote,
                "dstRemote": destination_path,
                "_async": True
            }
            if operation == Operation.COPY:
                method = Method.OPERATIONS_COPYFILE
                if createEmptySrcDirs:
                    params['createEmptySrcDirs'] = True
            elif operation == Operation.MOVE:
                method = Method.OPERATIONS_MOVEFILE
                if createEmptySrcDirs:
                    params['createEmptySrcDirs'] = True
                if deleteEmptySrcDirs:
                    params['deleteEmptySrcDirs'] = True
            else:
                raise ValueError("Operation not supported")

            job = self.__post(method, params)
            try:
                return f"Job started at {job['jobid']}"
            except KeyError:
                return str(job)
        else:

            params = {
                "srcFs": source,
                "dstFs": destination,
                "_async": True
            }

            if operation == Operation.COPY:
                method = Method.SYNC_COPY
                if createEmptySrcDirs:
                    params['createEmptySrcDirs'] = True
            elif operation == Operation.MOVE:
                method = Method.SYNC_MOVE
                if createEmptySrcDirs:
                    params['createEmptySrcDirs'] = True
                if deleteEmptySrcDirs:
                    params['deleteEmptySrcDirs'] = True
            elif operation == Operation.SYNC:
                method = Method.SYNC_SYNC
                if createEmptySrcDirs:
                    params['createEmptySrcDirs'] = True
            else:
                raise ValueError("Operation not supported")

            job = self.__post(
                method, params
            )
            try:
                return f"Job started at {job['jobid']}"
            except KeyError:
                return str(job)

    def copy(
            self,
            source: str,
            destination: str,
            createEmptySrcDirs: bool = False,
    ) -> str:
        return self.__operation(
            operation=Operation.COPY,
            source=source,
            destination=destination,
            createEmptySrcDirs=createEmptySrcDirs
        )

    def move(
            self,
            source: str,
            destination: str,
            createEmptySrcDirs: bool = False,
            deleteEmptySrcDirs: bool = False
    ) -> str:
        return self.__operation(
            operation=Operation.MOVE,
            source=source,
            destination=destination,
            createEmptySrcDirs=createEmptySrcDirs,
            deleteEmptySrcDirs=deleteEmptySrcDirs
        )

    def sync(
            self,
            source: str,
            destination: str,
            createEmptySrcDirs: bool = False
    ) -> str:
        return self.__operation(
            operation=Operation.SYNC,
            source=source,
            destination=destination,
            createEmptySrcDirs=createEmptySrcDirs
        )

    def get_core_stats(self, group: Optional[str] = None) -> CoreStats:
        if group is not None:
            stats = self.__post(Method.CORE_STATS, {"group": group})
        else:
            stats = self.__post(Method.CORE_STATS)
        return CoreStats.from_dict(stats)

    def stats(self) -> List[Transfer]:
        stats = self.get_core_stats()
        transferring: List[Transfer] = []

        if stats.transferring is not None:
            transferring = stats.transferring

        return transferring
