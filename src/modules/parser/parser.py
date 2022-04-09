import asyncio
from urllib.parse import urlencode

import aiohttp
from aiohttp import ClientConnectorError

import src.modules.parser.utils as utils
from src.modules.parser.utils import TorrentSite


class Parser:

    def __init__(self, site: TorrentSite):
        self.SITE = site
        self.URL = site.value
        self.__client = aiohttp.ClientSession()

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

        res = await self.__get_request(
            f"{url}/{user_uri}?{urlencode(params)}"
        )

        return utils.parse_site(
            request_text=res,
            site=self.SITE,
            **params
        )

    async def view(self, view_id: int) -> dict:
        res = await self.__get_request(
            f'{self.URL}/view/{view_id}'
        )

        return utils.parse_single(res, self.SITE)

    async def get_user(self, username: str) -> dict:
        res = await self.__get_request(
            f'{self.URL}/user/{username}'
        )

        return utils.parse_site(res, self.SITE)

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
