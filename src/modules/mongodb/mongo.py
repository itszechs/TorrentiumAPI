import re
import urllib.parse
from typing import Any

import pymongo
from bson.objectid import ObjectId


class MongoDb:
    SERVER_URL_REGEX = r"^(.*)://(.*):(.*)@(.*\.mongodb\.net)"

    def __init__(
            self,
            server_url: str,
            db_name: str,
            collection_name: str
    ) -> None:
        self.__db_name = db_name
        self.__collection_name = collection_name
        self.__split_server_url(server_url)

        # Connect to MongoDB
        self.__client = pymongo.MongoClient(
            self.server_url,
            retryWrites=True,
            w="majority"
        )

        print(self.__client.server_info())

        self.__db = self.__client[self.__db_name]
        self.__collection = self.__db[self.__collection_name]

    def __split_server_url(self, server_url) -> None:
        """
        Splits the server url into 3 parts
        - protocol
        - username
        - password
        - host
        """
        match = re.match(self.SERVER_URL_REGEX, server_url)
        if match:
            try:
                self.__protocol = match.group(1)
                self.__username = match.group(2)
                self.__password = match.group(3)
                self.__host = match.group(4)
            except IndexError:
                print("Invalid server url")
            self.__get_db_url()
        else:
            raise ValueError("Invalid server url")

    def __get_db_url(self) -> None:
        """
            Url encode the credentials and create the db url
        """
        username = urllib.parse.quote_plus(self.__username)
        password = urllib.parse.quote_plus(self.__password)
        self.server_url = f"{self.__protocol}://{username}:{password}@" \
                          f"{self.__host}/{self.__db_name}"

    def upsert(self, data: dict) -> None:
        """
            Insert data into the collection
            if it does not exist, otherwise update it
        """
        try:
            object_id = ObjectId(data["feed_id"])
            data.pop("feed_id")
            self.__collection.update_one(
                {"_id": object_id},
                {"$set": data},
                upsert=True
            )
        except KeyError:
            self.insert(data)

    def insert(self, data: dict) -> Any:
        """
        Inserts data into the collection
        and returns the inserted id
        Keep in mind, MongoDb does not have conflicts on insertion
        as they automatically append a unique id to the data
        Advised to use `upsert` function instead
        """
        return self.__collection.insert_one(data).inserted_id

    def query(self, query=None) -> Any:
        """
        Reads data from the collection
        If no query is provided, it will return all data
        """
        if query is None:
            query = {}
        return self.__collection.find(query)

    def update(self, query: dict, data: dict) -> int:
        """
        Updates data in the collection
        and returns modified count
        """
        return self.__collection.update_one(
            query,
            {"$set": data}
        ).modified_count

    def delete(self, object_id: str) -> bool:
        """
        Deletes data from the collection
        and returns deleted count
        """

        deleted = self.__collection.delete_one({
            '_id': ObjectId(object_id)
        }).deleted_count
        return False if deleted == 0 else True

    def drop(self) -> None:
        """
        Drops the collection
        """
        self.__collection.drop()
