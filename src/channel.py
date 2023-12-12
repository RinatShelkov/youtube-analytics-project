import json
import os
import pprint

from googleapiclient.discovery import build

from data.config import DATA_PATH


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv("API_KEY")
    youtube = build("youtube", "v3", developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.channel_id = channel_id
        data_channels = Channel.youtube.channels().list(id=self.channel_id, part="snippet").execute()
        self.title = ((data_channels.get("items")[0]).get("snippet")).get("title")
        self.description = ((data_channels.get("items")[0]).get("snippet")).get("description")
        self.url = "https://www.youtube.com/channel/" + channel_id
        data_channels_statistics = Channel.youtube.channels().list(id=self.channel_id, part="statistics").execute()
        self.subscribercount = ((data_channels_statistics.get("items")[0]).get("statistics")).get("subscriberCount")
        self.videocount = ((data_channels_statistics.get("items")[0]).get("statistics")).get("videoCount")
        self.viewcount = ((data_channels_statistics.get("items")[0]).get("statistics")).get("viewCount")
        pass

    def __str__(self):
        return f"'{self.title} ({self.url})'"

    def __add__(self, other):
        return int(self.subscribercount) + int(other.subscribercount)

    def __sub__(self, other):
        return int(self.subscribercount) - int(other.subscribercount)

    def __gt__(self, other):
        return int(self.subscribercount) > int(other.subscribercount)

    def __ge__(self, other):
        return int(self.subscribercount) > int(other.subscribercount)

    def __lt__(self, other):
        return int(self.subscribercount) < int(other.subscribercount)

    def __le__(self, other):
        return int(self.subscribercount) <= int(other.subscribercount)

    def __eq__(self, other):
        return int(self.subscribercount) == int(other.subscribercount)

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv("API_KEY")
        youtube = build("youtube", "v3", developerKey=api_key)
        return youtube

    def to_json(self, name_json):
        data = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscribercount": self.subscribercount,
            "videocount": self.videocount,
            "viewcount": self.viewcount,
        }
        with open(DATA_PATH.joinpath(name_json), "w") as f:
            json.dump(data, f, ensure_ascii=True)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        return pprint.pprint(Channel.youtube.channels().list(id=self.channel_id, part="snippet,statistics").execute())
