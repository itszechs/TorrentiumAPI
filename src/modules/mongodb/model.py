from typing import Optional

from pydantic import BaseModel


class Feed(BaseModel):
    feedId: Optional[str] = None
    title: str
    rssUrl: str
