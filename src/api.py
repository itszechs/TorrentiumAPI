from fastapi import FastAPI

from .routers import nyaa, sukebei, aria

app = FastAPI(
    title="TorrentiumAPI",
    description="""
    TorrentiumAPI is the backend for Torrentium Android app.
    It is a fast, simple, and powerful API for searching torrents on various sites.
    It also provides some additional functionality complementary to torrents.
    """,
    version="1.1.1",
    contact={
        "name": "zechs",
        "url": "https://itszechs.github.io/",
    }
)

app.include_router(nyaa.router)
app.include_router(sukebei.router)
app.include_router(aria.router)
