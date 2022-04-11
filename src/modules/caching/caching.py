import time
from typing import Union

TWO_MINS_IN_MILLIS = 120000


def current_time_in_millis() -> int:
    return int(time.time() * 1000)


class Caching:
    """
        In memory caching, cache is time sensitive.
        If the cache is not expired, it will be returned.
        If the cache is expired, it will be removed and a new one will be created.
        Cache lifetime is 2 minutes.

        Sticking with in memory cache and a short 2-minute cache lifetime
        due to the nature of the data we are dealing with here, site data updates very fast
        so doesn't make much sense of using a persistent cache or maintaining it for longer period of time.
    """

    def __init__(self) -> None:
        self.cache = []

    def get_cache(self, key: str) -> Union[dict, None]:
        for item in self.cache:
            if item['key'] == key:
                if item['time'] > current_time_in_millis() - TWO_MINS_IN_MILLIS:
                    print(f"Cache found {item['key']}")
                    return item['value']
                else:
                    print(f"Cache expired {item['key']}")
                    self.cache.remove(item)
                    return None
        print(f"Cache not found {key}")
        return None

    def set_cache(self, key: str, value: Union[str, dict]) -> None:
        self.cache.append({
            'key': key,
            'value': value,
            'time': current_time_in_millis()
        })
        print(f"New cache: {key}")

        # also remove any expired cache
        self.__clear_expired_cache()

    def __clear_expired_cache(self) -> None:
        for item in self.cache:
            if item['time'] < current_time_in_millis() - TWO_MINS_IN_MILLIS:
                print(f"Cache expired {item['key']}")
                self.cache.remove(item)

    def clear_cache(self) -> None:
        self.cache = []
