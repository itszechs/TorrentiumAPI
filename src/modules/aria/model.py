from dataclasses import dataclass
from typing import List

from pydantic import BaseModel


@dataclass
class AriaStats:
    num_active: int
    num_stopped: int
    num_waiting: int


class MessageResponse(BaseModel):
    message: str


class Download(BaseModel):
    gid: str
    name: str
    status: str
    progress: str
    downloaded: int
    size: int
    speed: str
    eta: str
    is_torrent: bool
    up_speed: str
    peers: int
    seeds: int
    leechs: int
    ratio: float


class DownloadsResponse(BaseModel):
    downloads: List[Download]


class Aria(BaseModel):
    waiting: int
    active: int


class Disk(BaseModel):
    total: int
    used: int
    free: int


class Network(BaseModel):
    down: int
    up: int
    total: int


class AriaStatsResponse(BaseModel):
    disk: Disk
    network: Network
    aria: Aria
    version: str
