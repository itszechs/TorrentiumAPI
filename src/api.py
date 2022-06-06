import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

from .routers import nyaa, sukebei, aria, \
    jackett, rclone

app = FastAPI(
    title="TorrentiumAPI",
    description="""
    TorrentiumAPI is the backend for Torrentium Android app.
    It is a fast, simple, and powerful API for searching torrents on various sites.
    It also provides some additional functionality complementary to torrents.
    """,
    version="1.2.0",
    contact={
        "name": "zechs",
        "url": "https://itszechs.github.io/",
    }
)

app.include_router(nyaa.router)
app.include_router(sukebei.router)
app.include_router(aria.router)

if os.path.exists('.env'):
    dotenv_path = Path('.env')
    load_dotenv(dotenv_path=dotenv_path)

if os.getenv('MONGODB_URL'):
    from .routers import rss

    app.include_router(rss.router)
else:
    print("MONGODB_URL is not set, rss router not included")

app.include_router(jackett.router)
app.include_router(rclone.router)
