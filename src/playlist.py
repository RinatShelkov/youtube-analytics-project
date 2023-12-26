import datetime
import os

import isodate
from googleapiclient.discovery import build


class PlayList:
    """- Реализуйте класс `PlayList`, который инициализируется _id_ плейлиста и имеет следующие публичные атрибуты:
    - название плейлиста
    - ссылку на плейлист"""

    api_key: str = os.getenv("API_KEY")
    youtube = build("youtube", "v3", developerKey=api_key)

    def __init__(self, id_playlist):
        self.id_playlist = id_playlist

        self.playlist_videos = (
            PlayList.youtube.playlistItems()
            .list(
                playlistId=self.id_playlist,
                part="contentDetails, snippet",
                maxResults=50,
            )
            .execute()
        )
        self.title = self.playlist_videos["items"][0]["snippet"]["title"].split(". ")[0]
        self.url = "https://www.youtube.com/playlist?list=" + self.id_playlist
        self.video_ids = [video["contentDetails"]["videoId"] for video in self.playlist_videos["items"]]

    @property
    def total_duration(self):
        """возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста
        (обращение как к свойству, использовать `@property`)"""

        video_response = (
            PlayList.youtube.videos().list(part="contentDetails,statistics", id=",".join(self.video_ids)).execute()
        )
        time_list = []
        for video in video_response["items"]:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video["contentDetails"]["duration"]
            duration = isodate.parse_duration(iso_8601_duration)
            time_list.append(duration)

        time_summ = sum(time_list, datetime.timedelta())
        return time_summ

    def show_best_video(self):
        """возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        like_count = 0
        id_url = ""

        for video_id in self.video_ids:
            video_response = PlayList.youtube.videos().list(part="statistics", id=video_id).execute()

            if int(video_response["items"][0]["statistics"]["likeCount"]) > like_count:
                like_count = int(video_response["items"][0]["statistics"]["likeCount"])
                id_url = video_response["items"][0]["id"]
        url = "https://youtu.be/" + id_url
        return url
