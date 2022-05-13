from dataclasses import dataclass
from typing import Dict


@dataclass
class Notification:
    title: str
    body: str
    topic: str

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "body": self.body,
            "topic": self.topic
        }
