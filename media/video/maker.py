import os
import random
from typing import Union
from operator import itemgetter

from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    VideoClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
    CompositeAudioClip,
    ColorClip
)

from moviepy.video.fx.resize import resize
from moviepy.video.fx.speedx import speedx
from moviepy.video.fx.crop import crop
from moviepy.video.fx.resize import resize
from moviepy.audio.fx.volumex import volumex

from utilities.shared import generate_random_file_name
from utilities.config.folder import OUTPUT_FOLDER, TEMP_FOLDER
from media.text.editor import auto_line_break
from content.markers.creator import Marker
import utilities.config.text as text_config

class VideoMaker:
    def __init__(self, video_path_or_size: Union[str, tuple[float, float]], duration=None):
        if isinstance(video_path_or_size, str):
            self.video = VideoFileClip(video_path_or_size, fps_source="fps")
        elif isinstance(video_path_or_size, tuple):
            if duration is None:
                raise ValueError("Se o video eh uma tupla, deve ser passado a duracao")
            
            size = video_path_or_size
            self.video = ColorClip(size, color=(255, 255, 255), duration=duration)


    def extract_random_chunk(self, duration: float) -> 'VideoMaker':
        # Get the file extension and directory from the video path
        video_duration = self.video.duration

        # Generate a random start time within the video duration
        start_time = random.uniform(0, video_duration - duration)

        # Calculate the end time based on the start time and duration
        end_time = start_time + duration

        subclip: VideoClip = self.video.subclip(start_time, end_time)
        subclip.duration = duration

        self.video = subclip

        return self
    
    def speed_up_video(self, by=2.0) -> 'VideoMaker':
        self.video = self.video.fx(speedx, factor=by)

        return self
    
    def crop_video(self, crop_proportion: float) -> 'VideoMaker':
        # Calculate the crop dimensions based on the given proportion
        width, height = self.video.size
        crop_width = int(height * crop_proportion)
        crop_height = int(height)
        x = (width // 2) - (crop_width // 2)
        y = 0

        # Crop the video clip
        self.video = self.video.fx(crop, x1=x, y1=y, x2=x + crop_width, y2=y + crop_height)

        return self

    def place_text(self, text: str, duration: float, offset=0.0, single_frame=False) -> 'VideoMaker':
        splitted_text = [text] if single_frame else auto_line_break(text, self.video.w)
        splitted_text_ratios = map(lambda x: len(x) / len(text), splitted_text)
        total_ratio = 0

        clips: list[TextClip] = []
        for string  in splitted_text:
            ratio = next(splitted_text_ratios)
            total_ratio += ratio
            current_duration = duration * ratio

            clip = TextClip(string, method="caption", size=self.video.size, font=text_config.FONT, color=text_config.COLOR, stroke_color=text_config.STROKE_COLOR, fontsize=text_config.FONT_SIZE)
            def resize_animation(t):
                return 1
            clip = clip.fx(resize, resize_animation)
            clip = clip.set_duration(current_duration) \
                       .on_color(size=(int(self.video.w * 0.9), self.video.h), color=(0,0,0), pos='center', col_opacity=0) \

            
            clips.append(clip)
        print("Total ratios:", total_ratio)

        txt_mov = concatenate_videoclips(clips, method="compose") \
                      .set_start(offset) \
                      .set_duration(duration) \
        
        self.video = CompositeVideoClip([self.video,txt_mov], use_bgclip=True)

        return self
    
    def remove_audio(self) -> 'VideoMaker':
        self.video = self.video.without_audio()
        return self


    def add_audio(self, audio_path: str, volume=1.0, duration=-1.0) -> 'VideoMaker':
        audio_clip = AudioFileClip(audio_path)

        if duration >= 0:
            # Get the file extension and directory from the video path
            video_duration = audio_clip.duration

            # Generate a random start time within the video duration
            start_time = random.uniform(0, video_duration - duration)

            # Calculate the end time based on the start time and duration
            end_time = start_time + duration

            audio_clip: AudioFileClip = audio_clip.subclip(start_time, end_time)
            audio_clip.duration = duration

        audio_clip = audio_clip.fx(volumex, volume)
        if self.video.audio:
            new_audio = CompositeAudioClip([self.video.audio, audio_clip])
            self.video = self.video.set_audio(new_audio)
        else:
            self.video = self.video.set_audio(audio_clip)

        return self
    
    def set_volume(self, amount: float):
        audio_clip = self.video.audio

        if not audio_clip: return self

        audio_clip = audio_clip.fx(volumex, amount)
        self.video.set_audio(audio_clip)
        return self

    
    def overlay_video(self, overlay_video: VideoClip, y: float, center: bool = False):
        # Resize the overlay_video to fit the width of self.video while maintaining the aspect ratio
        overlay_aspect_ratio = overlay_video.w / overlay_video.h
        overlay_width = self.video.w
        overlay_height = int(overlay_width / overlay_aspect_ratio)
        overlay_video = overlay_video.fx(resize, (overlay_width, overlay_height))

        y_position: float
        if center:
            # Calculate the y position to vertically center the video in the space (self.video.w, self.video.h - y)
            remaining = self.video.h - y
            if overlay_height < remaining:
                y_position = y + (remaining - overlay_height) / 2
            else:
                y_position = y - (overlay_height - remaining) / 2
        else:
            # Use the provided y value as the y position
            y_position = y

        # Composite the overlay_video on self.video
        self.video = CompositeVideoClip([self.video, overlay_video.set_position((0, y_position))])
        return self
    
    def overlay(self, top_video: VideoClip, bottom_video: VideoClip):
        # Combine two videos, top_video on top and bottom_video at the bottom,
        # with top_video taking all the width while keeping proportion

        # Calculate the size of the top video based on its width and height
        top_width, top_height = self.video.size
        aspect_ratio = top_width / top_height

        # Calculate the height of the top video to fit the full width of the final video
        final_width, final_height = self.video.size
        top_height = int(final_width / aspect_ratio)

        # Resize the top video to fit the calculated height while maintaining the aspect ratio
        top_video = top_video.fx(resize, (final_width, top_height))

        # Calculate the position to place the bottom video
        bottom_x = 0
        bottom_y = top_height

        self.video = CompositeVideoClip([
            top_video.set_position((0, 0)),
            bottom_video.set_position((bottom_x, bottom_y))
        ])
        return self

    def select_video_parts(self, markers: list[Marker], num_clips: int, min_duration: float, max_duration: float):
        # Filter markers with intensity at least 0.5
        markers = [m for m in markers if m["heatMarkerIntensityScoreNormalized"] >= 0.5]
        if not markers:
            return []
            
        # Sort markers in descending order by intensity
        markers.sort(key=itemgetter("heatMarkerIntensityScoreNormalized"), reverse=True)

        # Convert time from milliseconds to seconds
        for m in markers:
            m["timeRangeStartMillis"] /= 1000.0
            m["markerDurationMillis"] /= 1000.0
        
        clips: list[VideoClip] = []
        
        # Convert max_duration from seconds to milliseconds
        max_duration_millis = max_duration * 1000
        
        for m in markers:
            start_time = m["timeRangeStartMillis"] - 3  # start 3 seconds earlier
            end_time = start_time + m["markerDurationMillis"]
            
            # Extend the end_time if there's another marker close to the current marker's end
            for m_next in markers:
                if m_next["timeRangeStartMillis"] <= end_time + 5 and m_next["timeRangeStartMillis"] >= end_time:
                    end_time = m_next["timeRangeStartMillis"] + m_next["markerDurationMillis"]
            
            # Limit the duration of the clip
            if end_time - start_time > max_duration_millis:
                end_time = start_time + max_duration_millis
            else:
                end_time = start_time + min_duration
            
            clip = self.video.subclip(start_time, end_time)
            clips.append(clip)
                
            # Break the loop when the desired number of clips is reached
            if len(clips) == num_clips:
                break
                
        return clips
    
    def deploy(self):
        filename = generate_random_file_name("deployed", "mp4")
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        temp_audio_file = generate_random_file_name("audio", "mp3")
        temp_audio_file = os.path.join(TEMP_FOLDER, temp_audio_file)
        self.video.write_videofile(filepath, codec="libx265", temp_audiofile=temp_audio_file)

        return filepath