import os

from googleapiclient.discovery import build


class Video:
    """Инициализация реальными данными следующих атрибутов экземпляра класса `Video`:
    - id видео
    - название видео
    - ссылка на видео
    - количество просмотров
    - количество лайков"""

    api_key: str = os.getenv("API_KEY")
    youtube = build("youtube", "v3", developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""

        self.video_id = video_id  #
        self.video_response = (
            Video.youtube.videos().list(part="snippet,statistics,contentDetails,topicDetails", id=video_id).execute()
        )
        self.channel_id = self.video_response["items"][0]["snippet"]["channelId"]
        self.video_title = self.video_response["items"][0]["snippet"]["title"]  #
        self.view_count = self.video_response["items"][0]["statistics"]["viewCount"]  #
        self.like_count = self.video_response["items"][0]["statistics"]["likeCount"]  #
        self.comment_count = self.video_response["items"][0]["statistics"]["commentCount"]
        self.url = "https://www.youtube.com/channel/" + self.channel_id + "/" + self.video_id

    def __str__(self):
        return f"{self.video_title}"


class PLVideo(Video):
    """Инициализация реальными данными следующих атрибутов экземпляра класса `Video`:
    - id видео
    - название видео
    - ссылка на видео
    - количество просмотров
    - количество лайков
    - id плейлиста"""

    def __init__(self, video_id, playlist_id) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_videos = (
            Video.youtube.playlistItems()
            .list(
                playlistId=playlist_id,
                part="contentDetails, snippet",
                maxResults=50,
            )
            .execute()
        )
        for playlist in self.playlist_videos["items"]:
            if playlist["contentDetails"]["videoId"] == self.video_id:
                self.video_title = playlist["snippet"]["title"]
