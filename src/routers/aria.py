import base64
import binascii
import shutil

import psutil
from fastapi import APIRouter

from src.modules.aria.aria2c import Aria2c
from src.modules.aria.model import AriaStatsResponse, DownloadsResponse, MessageResponse

router = APIRouter(
    prefix="/api/v1/aria",
    tags=["Aria2c"]
)

aria2c = Aria2c()


@router.post(
    path="/add",
    response_model=MessageResponse
)
async def aria_add(uri: str):
    """
        Add any type of uri to aria2c.

        **uri** - must be encoded in base64

        Returns `gid` of the newly created download
    """
    try:
        decoded_uri = base64.b64decode(uri).decode("utf-8")
        try:
            response = await aria2c.add_uri(uris=[decoded_uri])
        except TypeError:
            return {"message": "Invalid uri"}
        try:
            gid = response['result']
            return {"message": gid}
        except KeyError:
            return {"message": response['error']['message']}
    except binascii.Error:
        return {"message": "URI must be encoded in Base64"}


@router.post(
    path="/pause",
    response_model=MessageResponse
)
async def aria_pause(gid: str):
    """
        Pause active download

        **gid** - plain string

        Returns `gid` of the paused download
    """
    response = await aria2c.pause(gid)
    try:
        gid = response['result']
        return {"message": gid}
    except KeyError:
        return {"message": response['error']['message']}


@router.post(
    path="/resume",
    response_model=MessageResponse
)
async def aria_resume(gid: str):
    """
        Resume active download

        **gid** - plain string

        Returns `gid` of the resumed download
    """
    response = await aria2c.pause(gid)
    try:
        gid = response['result']
        return {"message": gid}
    except KeyError:
        return {"message": response['error']['message']}


@router.post(
    path="/remove",
    response_model=MessageResponse
)
async def aria_remove(gid: str):
    """
        Remove active download

        **gid** - plain string

        Returns `gid` of the removed download
    """
    response = await aria2c.remove(gid)
    try:
        gid = response['result']
        return {"message": gid}
    except KeyError:
        return {"message": response['error']['message']}


@router.get(path="/downloads", response_model=DownloadsResponse)
async def aria_downloads():
    """
        Returns list of all downloads
    """
    return await aria2c.get_downloads()


@router.get(path="/stats", response_model=AriaStatsResponse)
async def aria_stats():
    """
        Returns storage stats, aria2c stats and data usages
    """

    info = await aria2c.get_global_stat()
    version = await aria2c.get_version()
    total, used, free = shutil.disk_usage('.')

    try:
        raw_network_data = psutil.net_io_counters(pernic=True)
        download = int(raw_network_data['eth0'][1])
        upload = int(raw_network_data['eth0'][0])
        bandwidth_total = download + upload
    except KeyError:
        download = 0
        upload = 0
        bandwidth_total = 0

    return {
        "disk": {
            "total": total,
            "used": used,
            "free": free
        },
        "network": {
            "down": download,
            "up": upload,
            "total": bandwidth_total
        },
        "aria": {
            "waiting": info.num_waiting,
            "active": info.num_active
        },
        "version": version
    }
