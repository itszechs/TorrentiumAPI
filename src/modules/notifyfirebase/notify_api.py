import json

import requests

from src.modules.notifyfirebase.apps import Apps
from src.modules.notifyfirebase.notification import Notification


class NotifyAPI:
    def __init__(self):
        self.__session = requests.Session()
        self.notify_firebase = "https://notify-firebase.herokuapp.com"

    def notify(self, app: Apps, notification: Notification) -> None:
        notify = self.__session.post(
            url=f"{self.notify_firebase}/api/v1/send/{app.value}",
            data=json.dumps(notification.to_dict())
        )
        if notify.status_code == 200:
            print("Notification sent.")
        else:
            print(f"Notification failed with error code {notify.status_code}")

    def notify_torrentium(self, notification: Notification) -> None:
        self.notify(
            app=Apps.TORRENTIUM,
            notification=notification
        )

    def notify_zplex(self, notification: Notification) -> None:
        self.notify(
            app=Apps.ZPLEX,
            notification=notification
        )
