import time
from datetime import datetime
from typing import Dict, List, Callable, Union

import feedparser

from src.modules.rss_reader.utils import verify_link, find_link


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
                    link = entry['link']

                    if not verify_link(link):
                        if find_link(entry['links']):
                            link = find_link(entry['links'])
                        else:
                            continue

                    rss['entries'].append({
                        "title": entry['title'],
                        "site": entry['id'],
                        "torrent": link,
                        "timestamp": entry['published']
                    })
                return rss
            except (TypeError, KeyError) as e:
                print("Error parsing RSS feed")
                print(e)
        else:
            print(f"Error parsing RSS feed: {parse.bozo_exception}")

        return None

    def __subscribe(self) -> None:

        if len(self.urls) == 0:
            print("No RSS feeds found")
            return

        date_format = "%a, %d %b %Y %H:%M:%S -0000"
        strp_last_updated = datetime.strptime(
            self.last_updated, date_format
        )
        for url in self.urls:
            count = 0
            rss = self.__parse(url)

            if rss is not None:
                for entry in rss['entries']:
                    strp_entry = datetime.strptime(
                        entry['timestamp'], date_format
                    )
                    if strp_last_updated <= strp_entry:
                        print(f"New post: {entry}")
                        if self._callback:
                            self._callback(dict(entry))
                        count += 1

            if count > 0:
                print(f'{self.last_updated} - {count} new entries found')
            else:
                print(f"{self.last_updated} - No new entries")

            time.sleep(10)  # wait 10 seconds
            print()
