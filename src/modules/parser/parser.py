import asyncio
from urllib.parse import urlencode

import aiohttp
from aiohttp import ClientConnectorError

import src.modules.parser.utils as utils
from src.modules.caching.caching import Caching
from src.modules.parser.utils import TorrentSite


class Parser:

    def __init__(self, site: TorrentSite):
        self.SITE = site
        self.URL = site.value
        self.__client = aiohttp.ClientSession()
        self.caching = Caching()

    def __del__(self):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.__client.close())
            else:
                loop.run_until_complete(self.__client.close())
        except Exception:
            pass

    async def search(
            self,
            keyword: str,
            **kwargs: str or int
    ) -> dict:
        url = self.URL

        user = kwargs.get('user', None)
        category = kwargs.get('category', 0)
        subcategory = kwargs.get('subcategory', 0)
        filters = kwargs.get('filter', 0)
        page = kwargs.get('page', 1)
        sort = kwargs.get('sort', 'id')
        order = kwargs.get('order', 'desc')

        if user:
            user_uri = f"user/{user}"
        else:
            user_uri = ""

        params = {
            "q": keyword,
            "c": f"{category}_{subcategory}",
            "f": filters,
            "p": page,
            "s": sort,
            "o": order
        }
        params_encoded = urlencode(params)

        cache_key = f"{self.SITE.name}_{user_uri}_{params_encoded}"
        cached = self.caching.get_cache(key=cache_key)

        if cached:
            return cached
        else:
            res = await self.__get_request(
                f'{url}/{user_uri}?{params_encoded}'
            )
            parsed = utils.parse_site(
                request_text=res,
                site=self.SITE,
                **params
            )
            self.caching.set_cache(key=cache_key, value=parsed)
            return parsed

    async def view(self, view_id: int) -> dict:
        cache_key = f"{self.SITE.name}_{view_id}"
        cached = self.caching.get_cache(key=cache_key)

        if cached:
            return cached
        else:
            res = await self.__get_request(
                f'{self.URL}/view/{view_id}'
            )
            parsed = utils.parse_single(res, self.SITE)
            self.caching.set_cache(key=cache_key, value=parsed)
            return parsed

    async def get_user(self, username: str) -> dict:
        cache_key = f"{self.SITE.name}_{username}"
        cached = self.caching.get_cache(key=cache_key)

        if cached:
            return cached
        else:
            res = await self.__get_request(
                f'{self.URL}/user/{username}'
            )
            parsed = utils.parse_site(res, self.SITE)
            self.caching.set_cache(key=cache_key, value=parsed)
            return parsed

    async def __get_request(self, url: str) -> str:

        try:
            async with self.__client.get(url) as response:
                return await response.text()
        except ClientConnectorError:
            raise ConnectionError(
                f"{self.SITE.name} is not available"
            )


class Nyaa(Parser):
    def __init__(self):
        super().__init__(TorrentSite.NYAA)


class Sukebei(Parser):
    def __init__(self):
        super().__init__(TorrentSite.SUKEBEI)
