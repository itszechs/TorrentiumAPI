from datetime import timedelta
from pathlib import Path
from typing import List


def human_readable_bytes(value: int) -> str:
    hr_value: float = value
    chosen_unit = "B"
    for unit in ("KiB", "MiB", "GiB", "TiB"):
        if hr_value > 1000:
            hr_value /= 1024
            chosen_unit = unit
        else:
            break
    return f"{hr_value:.{2}f}" + f" {chosen_unit}/s"


def parse_downloads(downloads: List[dict]):
    new_downloads = []
    for download in downloads:
        bittorrent = download.get("bittorrent", {})
        bittorrent_info = bittorrent.get("info", {})
        completed_length = int(download.get("completedLength", 0))
        connections = int(download.get("connections", 0))
        _dir = download.get("dir", "")
        download_speed = int(download.get("downloadSpeed", 0))
        files = download.get("files", [])
        gid = download.get("gid", "")
        num_seeders = int(download.get("numSeeders", 0))
        status: str = download.get("status", "")
        total_length = int(download.get("totalLength", 0))
        upload_length = int(download.get("uploadLength", 0))
        upload_speed = int(download.get("uploadSpeed", 0))

        try:
            percent = f"{str(round(((completed_length / total_length) * 100), 2))}%"
        except ZeroDivisionError:
            percent = "0.00%"

        try:
            eta = timedelta(seconds=int(
                total_length - completed_length) / download_speed
            )
        except ZeroDivisionError:
            eta = timedelta.max

        try:
            ratio = float(round((upload_length / completed_length), 2))
        except ZeroDivisionError:
            ratio = float(0.00)

        _download_name = ""
        _path = str(files[0].get("path", ""))

        if bittorrent and bittorrent_info:
            _download_name = bittorrent_info["name"]
        elif _path.startswith("[METADATA]"):
            _download_name = _path
        else:
            file_path = str(Path(files[0]['path']).absolute())
            dir_path = str(Path(_dir).absolute())
            if file_path.startswith(dir_path):
                start_pos = len(dir_path) + 1
                _download_name = Path(file_path[start_pos:]).parts[0]
            else:
                try:
                    _download_name = str(
                        files[0]['uris'][0]["uri"]
                    ).split("/")[-1]
                except IndexError:
                    pass

        new_downloads.append({
            "gid": gid,
            "name": _download_name,
            "status": status,
            "progress": percent,
            "downloaded": completed_length,
            "size": total_length,
            "speed": human_readable_bytes(download_speed),
            "up_speed": human_readable_bytes(upload_speed),
            "eta": eta,
            "is_torrent": bool(bittorrent),
            "peers": connections,
            "seeds": num_seeders,
            "leechs": num_seeders,
            "ratio": ratio
        })
    return {"downloads": new_downloads}
