from dataclasses import dataclass
from datetime import timedelta
from typing import List, Optional

from dataclasses_json import dataclass_json
from pydantic.main import BaseModel

from src.modules.rclone.utils import human_readable_bytes


@dataclass_json
@dataclass
class Version:
    arch: str
    decomposed: List[int]
    go_tags: str
    go_version: str
    is_beta: bool
    is_git: bool
    linking: str
    os: str
    version: str


@dataclass_json
@dataclass
class Remotes:
    remotes: List[str]


@dataclass_json
@dataclass
class JobsList:
    jobids: List[int]


@dataclass_json
@dataclass
class Transfer:
    name: str
    size: int
    bytes: Optional[int] = None
    speed: Optional[float] = None
    percentage: Optional[str] = None
    eta: Optional[int] = None
    group: Optional[str] = None

    @property
    def size_human(self) -> str:
        return human_readable_bytes(int(self.size))

    @property
    def bytes_human(self) -> str:
        if bytes is not None:
            return human_readable_bytes(int(self.bytes))
        return "0B"

    @property
    def progress(self) -> str:
        if self.percentage is None:
            return "0.00%"
        else:
            try:
                percent = int(self.bytes) / int(self.size) * 100
                return f"{str(round(percent, 2))}%"
            except ZeroDivisionError:
                return "0.00%"

    @property
    def speed_human(self) -> str:
        try:
            return f"{human_readable_bytes(int(self.speed))}/s"
        except (KeyError, TypeError):
            return "0.00 B/s"

    @property
    def eta_human(self) -> str:
        if self.eta is None or self.eta == 0:
            return "Inf"
        return str(timedelta(seconds=int(self.eta)))


@dataclass_json
@dataclass
class CoreStats:
    bytes: int
    checks: int
    deletedDirs: int
    deletes: int
    elapsedTime: float
    errors: int
    fatalError: bool
    renames: int
    retryError: bool
    speed: int
    totalBytes: int
    totalChecks: int
    totalTransfers: int
    transferTime: int
    transfers: int
    eta: Optional[int] = None
    transferring: Optional[List[Transfer]] = None


class TransferResponse(BaseModel):
    name: str
    size: int
    bytes: Optional[int] = None
    speed: Optional[float] = None
    percentage: Optional[str] = None
    eta: Optional[int] = None
    group: Optional[str] = None
    size_human: str
    bytes_human: str
    progress: str
    speed_human: str
    eta_human: str
