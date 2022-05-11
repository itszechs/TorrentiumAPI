import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

from src.modules.mongodb.mongo import MongoDb
from src.modules.rss_reader.model import MessageResponse, Subscription
from src.modules.rss_reader.utils import verify_link

if os.path.exists('.env'):
    dotenv_path = Path('.env')
    load_dotenv(dotenv_path=dotenv_path)

rss = MongoDb(
    server_url=os.getenv('MONGODB_URL'),
    db_name="Torrentium",
    collection_name="rss_feeds"
)

router = APIRouter(
    prefix="/api/v1/rss",
    tags=["Rss Feeds"]
)


@router.post(
    path="/subscribe",
    response_model=MessageResponse
)
async def subscribe(
        title: str,
        rss_url: str
):
    """
    Subscribe to a rss feed
    """
    if not title or not rss_url:
        raise HTTPException(
            status_code=400,
            detail="Title and rss url are required"
        )

    if not verify_link(rss_url):
        raise HTTPException(
            status_code=400,
            detail="Invalid or Incompatible rss url"
        )

    rss.upsert(data={
        "title": title,
        "rss_url": rss_url
    })
    return {"message": "Subscribed"}


@router.post(
    path="/unsubscribe",
    response_model=MessageResponse
)
async def unsubscribe(feed_id: str):
    """
    Unsubscribe to a rss feed
    """
    if not feed_id:
        raise HTTPException(
            status_code=400,
            detail="Feed id is required"
        )

    res = rss.delete(feed_id)

    if res:
        return {"message": "Unsubscribed"}

    raise HTTPException(
        status_code=404,
        detail="Rss feed not found"
    )


@router.get(
    path="/subscriptions",
    response_model=List[Subscription]
)
async def subscriptions():
    """
    Get all subscriptions
    """
    feeds = []

    for feed in rss.query():
        feeds.append({
            "feed_id": str(feed["_id"]),
            "title": feed["title"],
            "rss_url": feed["rss_url"]
        })

    return feeds
