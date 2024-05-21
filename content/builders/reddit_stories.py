import re
import os
from typing import Optional

from content.reddit.reader import RedditReader
from content.youtube.handler import YoutubeHandler
from media.audio.maker import from_text, concatenate_audios
from media.video.maker import VideoMaker
from utilities.config import reddit as reddit_config
from utilities.persistence.manager import PersistenceManager
from utilities.types.languages import SupportedLanguages
from utilities.types.reddit_types import RedditStoryConfig
from translate import Translator
from media.text.editor import sanitize, remove_abbreviation, remove_markdown, remove_readable_ponctuation, remove_urls
    

class RedditStoriesBuilder:
    def __init__(self, video_config: RedditStoryConfig) -> None:
        self.video_config = video_config
        self.youtube = YoutubeHandler()


    def deploy(self):
        self.reddit.deploy_used_items()

    def _get_content(self, persistence: PersistenceManager):
        self.reddit = RedditReader(persistence)
        content = self.reddit.sample(self.video_config)

        source_language = self.video_config['lang']
        content = list(map(
            lambda x: sanitize(x, source_language, pipes=[
                remove_markdown,
                remove_urls,
                remove_abbreviation,
            ]),
            content
        ))

        return content
    
    def _insert_subreddit_name(self, content: list[str]):
        subreddit = self.video_config['reddit']
        readable_name = subreddit['readable_name']
        subname_position = subreddit['subname_position']
        content.insert(subname_position, readable_name)

        return content
    
    def _translate_content(self, content: list[str], translate_to: SupportedLanguages):
        from_language: SupportedLanguages = self.video_config['lang']

        translator = Translator(from_language, translate_to)
        return list(map(translator.translate, content))
    
    def _get_audios(self, content: list[str], translate_to: SupportedLanguages):
        content = list(map(
            lambda x: sanitize(x, translate_to, pipes=[
                remove_readable_ponctuation
            ]),
            content
        ))

        audios = list(map(lambda x: re.sub(r"\[(.+)\]\(.+\)", r"\1", x), content))
        audios = list(map(lambda x: from_text(x, reddit_config.AUDIO_SPEED_UP, translate_to), content))

        total_length = 0
        for audio in audios:
            total_length += audio[0]
            total_length += reddit_config.AUDIO_GAP

        return audios, total_length
    
    def _initialize_background(self, length: float, speed_up: float):
        background = self.youtube.random('long')
        video = VideoMaker(background) \
                    .extract_random_chunk(length) \
                    .crop_video(9 / 16) \
                    .speed_up_video(by=speed_up)
        
        return video
    
    def _place_texts(self, video: VideoMaker, audios: list[tuple[float, str]], content: list[str]):
        offset = 0
        for index, text in enumerate(content):
            audio_length = audios[index][0]
            video = video.place_text(text, audio_length, offset)
            offset += audio_length + reddit_config.AUDIO_GAP

        return video
    
    def _add_audio(self, video: VideoMaker, audios: list[tuple[float, str]]):
        background_audio_path = self.youtube.random_song()

        audio_paths = map(lambda a: a[1], audios)
        audio_path = concatenate_audios(audio_paths, gap=reddit_config.AUDIO_GAP)
        videopath = video.remove_audio() \
             .add_audio(background_audio_path, reddit_config.BACKGROUND_VIDEO_VOLUME, 35) \
             .add_audio(audio_path) \
             .deploy()
        
        return videopath
    
    def build(self, persistence: PersistenceManager, translate_to: Optional[SupportedLanguages]) -> str:
        if not translate_to: return ''
        content = self._get_content(persistence)
        content = self._insert_subreddit_name(content)
        content = self._translate_content(content, translate_to)

        audios, total_length = self._get_audios(content, translate_to)
        
        video = self._initialize_background(
            total_length * reddit_config.BACKGROUND_VIDEO_SPEED_UP * reddit_config.AUDIO_SPEED_UP,
            reddit_config.BACKGROUND_VIDEO_SPEED_UP
        )
        video = self._place_texts(video, audios, content)
        videopath = self._add_audio(video, audios)
        
        return os.path.abspath(videopath)
