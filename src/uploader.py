# sys.argv[1] is gid
# sys.argv[2] is downloadName
# sys.argv[3] is sourcePath

import sys
import time
from datetime import datetime

from src.modules.rclone.rclone_rc import RcloneRC

CURRENT_MONTH = datetime.now().strftime('%B')
CURRENT_YEAR = datetime.now().year
MONTH_YEAR_FOLDER = f"{CURRENT_MONTH} - {CURRENT_YEAR}"

rclone = RcloneRC()


def log(msg: str) -> None:
    timestamp = time.strftime("%H:%M:%S")
    print(f"[ ARIA2C ] [{timestamp}] {msg}")


if len(sys.argv) == 4:
    # dirs
    source = str(sys.argv[3])

    log(f"Download with gid {sys.argv[1]} finished " +
        f"downloading {sys.argv[2]}, " +
        f"saved in`{source}`")

elif len(sys.argv) == 3:
    #  files

    source = f"/app/aria2/{str(sys.argv[2])}"

    log(f"Download with gid {sys.argv[1]} finished " +
        f"downloading {sys.argv[2]}, " +
        f"saved in`{source}`")
else:
    print("Error: Need at-least two arguments.")
    sys.exit(1)

log(rclone.move(
    source=source,
    destination=f"upload:{MONTH_YEAR_FOLDER}/{str(sys.argv[2])}",
    deleteEmptySrcDirs=True
))
