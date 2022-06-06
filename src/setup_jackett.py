import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv

from src.modules.jackett_api.jackett import JackettApi

jackett = JackettApi()

if os.path.exists(".env"):
    dotenv_path = Path(".env")
    load_dotenv(dotenv_path=dotenv_path)

default_trackers = ["eztv", "kickasstorrents-to", "limetorrents",
                    "nyaasi", "rarbg", "rutracker-ru",
                    "sukebeinyaasi", "thepiratebay", "yts"]

if os.getenv("TRACKERS_LIST"):
    list_of_trackers = os.getenv("TRACKERS_LIST").split(",")
else:
    list_of_trackers = default_trackers

all_trackers = [
    index['id']
    for index in jackett.get_indexers()
    if index["type"] == "public"
]


def configure_trackers(trackers: List[str]) -> int:
    """
    Configure trackers in Jackett
    :param trackers: List of trackers
    :return: Number of trackers configured
    """
    added = 0
    for tracker in trackers:
        if tracker in all_trackers:
            config = jackett.get_indexer(tracker)
            post = jackett.post_indexer(tracker, config)
            if post:
                added += 1
            print(f"{tracker} was{' ' if post is True else ' not '}added.")
        else:
            print(f"{tracker} is not a public tracker or is not supported by Jackett." +
                  " Skipping...")
    return added


print("Setting up trackers...")

configured = configure_trackers(trackers=list_of_trackers)

if configured == 0:
    print("No trackers were configured.")
    print("Adding defaults...")
    configured = configure_trackers(trackers=default_trackers)
    print(f"{configured} trackers were configured.")
else:
    print(f"{configured} trackers were configured.")
