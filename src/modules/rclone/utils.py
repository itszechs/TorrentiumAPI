import math
import os
from typing import Tuple


def split_path(path: str) -> Tuple[str, str]:
    _path = path

    if _path.startswith("/"):
        remote = "/"
    else:
        try:
            remote, _path = path.split(":", 1)
            remote += ":"
        except ValueError:
            remote = os.getcwd()

    if remote != "/":
        _path = _path.replace(remote, "")

    if not _path.startswith("/"):
        _path = "/" + _path

    return remote, _path


def human_readable_bytes(byte: int) -> str:
    if byte == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB")
    i = int(math.floor(math.log(byte, 1024)))
    p = math.pow(1000, i)
    s = round(byte / p, 2)
    return f"{s} {size_name[i]}"
