import re
import requests
from typing import TypedDict

class Marker(TypedDict):
    timeRangeStartMillis: float
    markerDurationMillis: float
    heatMarkerIntensityScoreNormalized: float

class MarkerCreator:
    BASE_URL = "https://yt.lemnoslife.com/videos?part=mostReplayed&id=%s"

    def __init__(self, video_url: str) -> None:
        self.video_id = self.get_youtube_video_id(video_url)

    def get_youtube_video_id(self, url: str):
        """
        Returns the Video ID from a YouTube URL.
        """
        youtube_id_match = re.search(r'(?<=v=)[^&#]+', url)
        youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', url)
        trailer_id = youtube_id_match.group(0) if youtube_id_match else None

        return trailer_id

    def get_markers(self):
        resp = requests.get(self.BASE_URL % self.video_id)
        resp_json = resp.json()
        return [x['heatMarkerRenderer'] for x in resp_json['items'][0]['mostReplayed']['heatMarkers']]
