# sys.argv[1] is gid
# sys.argv[2] is downloadName
# sys.argv[3] is sourcePath
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Union, Dict

import anitopy as anitopy
import requests as requests
from dotenv import load_dotenv

from src.modules.rclone.rclone_rc import RcloneRC

if os.path.exists('.env'):
    dotenv_path = Path('.env')
    load_dotenv(dotenv_path=dotenv_path)

CURRENT_MONTH = datetime.now().strftime('%B')
CURRENT_YEAR = datetime.now().year
MONTH_YEAR_FOLDER = f"{CURRENT_MONTH} - {CURRENT_YEAR}"
TMDB_API = "https://api.themoviedb.org/3"
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

rclone = RcloneRC()
session = requests.Session()


def parse_name(name: str) -> Union[Dict, None]:
    """
    Parse the name of the torrent.
    """
    try:
        # to handle any 'versioning'
        name = re.sub(r"(v\d)", "", name)
        parse = anitopy.parse(name)

        return {
            'title': parse['anime_title'],
            'season': parse.get('anime_season', '01'),
            'episode': parse['episode_number'],
        }
    except KeyError:
        print(f"Error: {name}")
        return None


def search_anime(name: str) -> Union[Dict, None]:
    """
    Get the TV show from the TMDB API.
    """
    print(f"Searching for {name}")
    tmdb = session.get(
        url=f"{TMDB_API}/search/tv",
        params={
            "api_key": TMDB_API_KEY,
            "query": name
        }
    )
    try:
        if tmdb.status_code == 200:
            tv = tmdb.json()['results'][0]
            return {
                'name': tv['name'],
                'tmdb_id': tv['id'],
            }
    except IndexError:
        print(f"Error: {name}")

    return None


def get_episode(
        tv_id: int,
        season_number: int,
        episode_number: int
) -> Union[str, None]:
    """
    Get the TV show from the TMDB API.
    """
    print(f"Searching for S{season_number}E{episode_number} in {tv_id}")
    tmdb = session.get(
        url=f"{TMDB_API}/tv/{tv_id}/season/{season_number}/episode/{episode_number}",
        params={"api_key": TMDB_API_KEY}
    )
    if tmdb.status_code == 200:
        return tmdb.json()['name']
    else:
        print(f"Error: {tmdb.status_code}")
    return None


def log(msg: str) -> None:
    timestamp = time.strftime("%H:%M:%S")
    print(f"[ ARIA2C ] [{timestamp}] {msg}")


destination = f"upload:{MONTH_YEAR_FOLDER}/{str(sys.argv[2])}"
if len(sys.argv) == 4:
    # dirs
    source = str(sys.argv[3])

    log(f"Download with gid {sys.argv[1]} finished " +
        f"downloading {sys.argv[2]}, " +
        f"saved in`{source}`")

elif len(sys.argv) == 3:
    #  files

    source = f"/app/aria2/{str(sys.argv[2])}"
    source_zplex = f"/app/zplex/{str(sys.argv[2])}"

    if os.path.exists(source_zplex):
        source = source_zplex
        parsed = parse_name(sys.argv[2])
        if parsed:
            anime = search_anime(parsed['title'])
            if anime:
                folder = f"{anime['tmdb_id']} - {anime['name']} - TV"
                file_ext = sys.argv[2].split('.')[-1]
                file_name = f"S{parsed['season']}E{parsed['episode']}.{file_ext}"

                episode = get_episode(
                    tv_id=anime['tmdb_id'],
                    season_number=parsed['season'],
                    episode_number=parsed['episode']
                )
                if episode and not episode == "":
                    file_name = f"S{parsed['season']}E{parsed['episode']} - {episode}.{file_ext}"
                else:
                    file_name = f"S{parsed['season']}E{parsed['episode']}.{file_ext}"
                destination = f"zplex:/TV Shows/{folder}/{file_name}"

    log(f"Download with gid {sys.argv[1]} finished " +
        f"downloading {sys.argv[2]}, " +
        f"saved in`{source}`")
else:
    print("Error: Need at-least two arguments.")
    sys.exit(1)

log(rclone.move(
    source=source,
    destination=destination,
    deleteEmptySrcDirs=True
))
