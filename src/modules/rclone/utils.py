import os
from typing import Tuple


def split_path(path: str) -> Tuple[str, str]:
    if path.startswith("/"):
        remote = "/"
    else:
        try:
            remote, _path = path.split(":", 1)
            remote += ":"
        except ValueError:
            remote = os.getcwd()

    _path = path.replace(os.getcwd(), "")

    if remote != "/":
        _path = _path.replace(remote, "")

    if not _path.startswith("/"):
        _path = "/" + _path

    return remote, _path
