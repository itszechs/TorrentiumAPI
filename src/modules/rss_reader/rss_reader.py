import time
from typing import Dict, List, Callable, Union

import feedparser


class RssReader:
    def __init__(
            self,
            urls: List[str],
            last_updated: str,
            callback: Callable = None
    ) -> None:
        self.urls = urls
        self.last_updated = last_updated
        self._callback = callback
        self.__subscribe()

    def __parse(self, url) -> Union[Dict, None]:
        parse = feedparser.parse(url)
        rss = {}
        if not parse.bozo:
            try:
                rss['url'] = parse.feed.link
                rss['title'] = parse.feed.title
                rss['entries'] = []

                for entry in parse.entries:
                    rss['entries'].append({
                        "title": entry['title'],
                        "id": entry['id'],
                        "link": entry['link'],
                        "timestamp": entry['published']
                    })
                return rss
            except (TypeError, KeyError):
                return None
        else:
            raise Exception(f"Error parsing RSS feed: {parse.bozo_exception}")

    def __subscribe(self) -> None:
        for url in self.urls:
            count = 0
            rss = self.__parse(url)

            if rss is not None:
                for entry in rss['entries']:
                    if self.last_updated <= entry['timestamp']:
                        print(f"New post: {entry}")
                        if self._callback:
                            self._callback(dict(entry))
                        count += 1

                if count > 0:
                    print(f'{count} new entries found')
                else:
                    print("No new entries")
            else:
                print("Error parsing RSS feed")

            time.sleep(10)  # wait 10 seconds
            print()
