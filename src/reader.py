import os
import time
from datetime import datetime
from pathlib import Path
from typing import List

import requests
from dotenv import load_dotenv

from src.modules.aria.aria2c import Aria2c
from src.modules.mongodb.mongo import MongoDb
from src.modules.notifyfirebase.notification import Notification
from src.modules.notifyfirebase.notify_api import NotifyAPI
from src.modules.rss_reader.rss_reader import RssReader

if os.path.exists('.env'):
    dotenv_path = Path('.env')
    load_dotenv(dotenv_path=dotenv_path)

APP_NAME = os.getenv('APP_NAME')
MONGODB_URL = os.getenv('MONGODB_URL')
PORT = os.getenv('PORT', 5000)

if not MONGODB_URL:
    print("MONGODB_URL are not set.")
    print("Exiting RssReader...")
    exit(0)

session = requests.Session()
notify_api = NotifyAPI()
aria2c = Aria2c()
mongo = MongoDb(
    server_url=MONGODB_URL,
    db_name="Torrentium",
    collection_name="rss_feeds"
)


def update_timestamp() -> str:
    return datetime.now().strftime(
        "%a, %d %b %Y %H:%M:%S -0000"
    )


def get_feeds() -> List[str]:
    return [
        feed['rss_url']
        for feed in mongo.query()
    ]


def aria_add(raw_link: str) -> None:
    try:
        response = aria2c.add_uri(
            uris=[raw_link],
            options={
                "dir": "/app/zplex"
            }
        )
        try:
            gid = response['result']
            print(f"Download added at gid: {gid}")
        except KeyError:
            print(response['error']['message'])
    except TypeError:
        print("Invalid uri")


def rss_add_torrent(feed: dict) -> None:
    title = feed['title']
    link = feed['torrent']
    print(f"RSS Callback: {title} - {link}")

    if link.startswith('magnet') or link.endswith('.torrent'):
        aria_add(link)
        notify_api.notify_torrentium(
            notification=Notification(
                title="New feed",
                body=f"\"{title}\" download started",
                topic=f"rss_{APP_NAME}"
            )
        )
    else:
        print(f"Feed: \"{title}\" does not contain a magnet or torrent link. Skipping...")


if __name__ == "__main__":

    timestamp = update_timestamp()

    while True:
        feeds = get_feeds()
        if len(feeds) == 0:
            print("No feeds found")
        else:
            RssReader(
                urls=feeds,
                last_updated=timestamp,
                callback=rss_add_torrent
            )
        timestamp = update_timestamp()
        # sleep 15 minutes
        time.sleep(15 * 60)
