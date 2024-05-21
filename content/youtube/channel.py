import pytube

class Channel:
    def __init__(self, channel_url: str):
        self.channel = pytube.Playlist(channel_url)

    def next(self, seen_videos: list[str]):
        videos = self.channel.videos #sorted(self.channel.videos, key=lambda y: y.views, reverse=True)
        videos = filter(lambda video: video.video_id not in seen_videos, videos)
        return next(videos)