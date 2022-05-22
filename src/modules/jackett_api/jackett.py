from typing import Any, List, Dict
from typing import Optional

import requests
from requests import Response


class JackettApi:
    def __init__(
            self,
            host: str = "http://localhost",
            port: Optional[int] = 9117
    ) -> None:
        url = host

        if port is not None:
            url += f":{port}"

        self.jackett_api = url
        self.session = requests.Session()

    def __request(
            self,
            method,
            endpoint,
            params: Optional[Any] = None,
            json: Optional[Any] = None
    ) -> Response:
        """
        Make a request to the Jackett API
        :param endpoint: The endpoint to request
        :param json: The params of the request
        :return: The response of the request
        """
        if not endpoint.startswith("/"):
            raise ValueError("Endpoint must start with a /")

        return self.session.request(
            method=method,
            url=f"{self.jackett_api}{endpoint}",
            json=json,
            params=params
        )

    def get(
            self, endpoint,
            params: Optional[Any] = None,
            json: Optional[Any] = None
    ) -> Response:
        """
            Make a GET request directly to Jackett API
        """

        return self.__request("GET", endpoint, params, json)

    def post(
            self, endpoint,
            params: Optional[Any] = None,
            json: Optional[Any] = None
    ) -> Response:
        """
            Make a POST request directly to Jackett API
        """

        return self.__request("POST", endpoint, params, json)

    def delete(
            self, endpoint,
            params: Optional[Any] = None,
            json: Optional[Any] = None
    ) -> Response:
        """
            Make a DELETE request directly to Jackett API
        """

        return self.__request("DELETE", endpoint, params, json)

    def put(
            self, endpoint,
            params: Optional[Any] = None,
            json: Optional[Any] = None
    ) -> Response:
        """
            Make a PUT request directly to Jackett API
        """

        return self.__request("PUT", endpoint, params, json)

    def post_indexer(self, name: str, config: List[Dict]) -> bool:
        """
        Add an indexer to jackett
        :param name: The name of the indexer
        :param config: The config of the indexer
        :return: True if the indexer was added, False otherwise
        """
        response = self.session.post(
            url=f"{self.jackett_api}/api/v2.0/indexers/{name}/config",
            json=config
        )
        return response.status_code == 204

    def get_indexer(self, name: str) -> List[Dict]:
        """
        Get the config of an indexer
        :param name: The name of the indexer
        :return: The config of the indexer
        """
        response = self.session.get(
            url=f"{self.jackett_api}/api/v2.0/indexers/{name}/config"
        )
        return response.json()

    def get_indexers(self) -> List[str]:
        """
            Get list of all indexers
            :return: List of all indexers
        """
        response = self.session.get(
            url=f"{self.jackett_api}/api/v2.0/indexers"
        )
        return response.json()
