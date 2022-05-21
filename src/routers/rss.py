import json
import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi import Response

from src.modules.mongodb.model import Feed
from src.modules.mongodb.mongo import MongoDb
from src.modules.rss_reader.model import MessageResponse, Subscription

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
async def subscribe(feed: Feed):
    """
    Subscribe to a rss feed
    """
    if not feed.title or not feed.rssUrl:
        return Response(
            content=json.dumps({"message": "Missing title or rss url"}),
            status_code=400
        )

    data = {
        "title": feed.title,
        "rss_url": feed.rssUrl
    }

    if feed.feedId is not None:
        data["feed_id"] = feed.feedId

    rss.upsert(data)

    return Response(
        content=json.dumps({"message": "Subscribed"}),
        status_code=200
    )


@router.post(
    path="/unsubscribe",
    response_model=MessageResponse
)
async def unsubscribe(feed_id: str):
    """
    Unsubscribe to a rss feed
    """
    if not feed_id:
        return Response(
            content=json.dumps({"message": "Feed id is required"}),
            status_code=400
        )

    res = rss.delete(feed_id)

    if res:
        return Response(
            content=json.dumps({"message": "Unsubscribed"}),
            status_code=200
        )
    return Response(
        content=json.dumps({"message": "Rss feed not found"}),
        status_code=404,

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
