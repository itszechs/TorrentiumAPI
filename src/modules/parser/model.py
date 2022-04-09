from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class Type(str, Enum):
    DEFAULT = "default"
    REMAKE = "remake"
    TRUSTED = "trusted"


class TorrentItem(BaseModel):
    id: int
    category: str
    url: str
    name: str
    download_url: str
    magnet: str
    size: str
    date: str
    seeders: int
    leechers: int
    completed_downloads: int
    type: str


class NyaaResponse(BaseModel):
    total_page: Optional[int]
    keyword: str
    category: int
    subcategory: int
    page: int
    filters: int
    sort: str
    order: str
    torrents: Optional[List[TorrentItem]]
    error: Optional[str]


class SukebeiResponse(NyaaResponse):
    pass


class Comment(BaseModel):
    author: str
    time: str
    text: str
    image: str


class FilesList(BaseModel):
    file: str
    size: str


class TorrentResponse(BaseModel):
    title: str
    category: str
    uploader: str
    uploader_profile: str
    website: str
    size: str
    date: str
    seeders: int
    leechers: int
    completed: int
    hash: str
    magnet: str
    comments: List[Comment]
    description: str
    files_list: List[FilesList]
