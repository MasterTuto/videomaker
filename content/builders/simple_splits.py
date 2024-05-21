
import pytube.exceptions

from typing import TypedDict

from content.youtube.handler import YoutubeHandler
from media.video.maker import VideoMaker
from utilities.persistence.manager import PersistenceManager
from utilities.config.folder import TEMP_FOLDER
from content.markers.creator import MarkerCreator

class SimpleSplitsConfig(TypedDict):
    channel_url: str

class SimpleSplitsBuilder:
    def __init__(self, video_config: SimpleSplitsConfig):
        self.video_config = video_config
        self.youtube = YoutubeHandler()

    def deploy(self):
        self.seen_videos_persistence.commit()

    def get_content_video_data(self):
        seen_video_ids = self.seen_videos_persistence.content
        random_video = self.youtube.channel(self.video_config['channel_url']).next(seen_video_ids)
        self.seen_videos_persistence.append(random_video.video_id)

        try:
            ytvideo = self.youtube.download(random_video.watch_url, output_folder=TEMP_FOLDER)
        except (
            pytube.exceptions.RegexMatchError,
            pytube.exceptions.MembersOnly,
            pytube.exceptions.AgeRestrictedError
        ) as e:
            print(e)
            return None
        marker_creator = MarkerCreator(random_video.watch_url)
        content_video_data = VideoMaker(ytvideo)
        try:
            markers = marker_creator.get_markers()
            content_video_data = content_video_data.select_video_parts(markers, 1, 60, 90)[0]
        except TypeError:
            content_video_data = content_video_data.extract_random_chunk(70).video
        
        return random_video.title, content_video_data
    
    def get_good_video(self, video_duration: float):
        while True:
            try:
                good_video_source = self.youtube.random()
                break
            except (
                pytube.exceptions.AgeRestrictedError,
                pytube.exceptions.MembersOnly,
                pytube.exceptions.RegexMatchError,
            ):
                pass
        
        random_good_video = VideoMaker(good_video_source) \
                    .extract_random_chunk(video_duration) \
                    .crop_video(9 / 16).video
        
        return random_good_video

    def build(self, seen_videos_persistence: PersistenceManager, translate_to):
        self.seen_videos_persistence = seen_videos_persistence
        
        content_video_data = self.get_content_video_data()
        while content_video_data is None:
            content_video_data = self.get_content_video_data()

        content_video_title, content_video = content_video_data
        

        video_duration: float = content_video.duration

        good_video = self.get_good_video(video_duration)
    
        video = VideoMaker((1080, 1920), duration=video_duration) \
            .overlay_video(good_video, 0, False) \
            .overlay_video(content_video, 1920/2, False) \
            .place_text(content_video_title, video_duration, 0, single_frame=True) \
            .set_volume(1)
        
        return video.deploy()




        

        
        
        
