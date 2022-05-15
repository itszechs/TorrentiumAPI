from typing import Any, Optional
from typing import Dict

import requests

from src.modules.rclone.method import Method
from src.modules.rclone.model import Version, Remotes, JobsList


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

    def __post(self, method: Method, params: Dict[Any] = None):
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
