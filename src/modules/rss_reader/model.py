from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str


class Subscription(BaseModel):
    feed_id: str
    title: str
    rss_url: str
