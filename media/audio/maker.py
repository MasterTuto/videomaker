import os
import math

from mutagen.mp3 import MP3
from pydub import AudioSegment
import librosa
import pyrubberband
import soundfile as sf
from scipy.io import wavfile
import librosa, numpy as np

from utilities.shared import generate_random_file_name
from utilities.config.folder import TEMP_FOLDER
import media.tts.manager as tts_manager

def from_text(text: str, speed: float, lang: str='en'):
    audio, already_sped_up = tts_manager.generate_audio(text, lang, speed)

    audio_name = generate_random_file_name("audio", "mp3")
    fpath = os.path.join(TEMP_FOLDER, audio_name)

    with open(fpath, 'wb') as f:
        f.write(audio)

    if not already_sped_up:
        fpath = speed_up_audio(fpath, speed)

    audio_length = get_audio_length(fpath)

    return audio_length, fpath

def get_audio_length(file_path: str) -> float:
    audio = MP3(file_path)
    length_in_seconds = audio.info.length
    return length_in_seconds


def concatenate_audios(audio_paths, gap: float=0):
    audio_segments = []

    # Load and append each audio segment
    for path in audio_paths:
        audio_segment = AudioSegment.from_file(path, format="mp3")
        audio_segments.append(audio_segment)

        # Add a silence gap between segments
        silence = AudioSegment.silent(duration=math.floor(gap * 1000))  # Convert gap to milliseconds
        audio_segments.append(silence)

    # Concatenate the audio segments
    concatenated_audio = AudioSegment.empty()
    for segment in audio_segments:
        concatenated_audio += segment

    # Create a new file name for the concatenated audio
    new_file_name = generate_random_file_name("audio", "mp3")
    new_file_path = os.path.join(TEMP_FOLDER, new_file_name)

    # Export the concatenated audio to a new file
    concatenated_audio.export(new_file_path, format="mp3")

    return new_file_path

def speed_up_audio(audio_path: str, by: float=1):
    song, fs = librosa.load(audio_path)

    song_2_times_faster = librosa.effects.time_stretch(song, rate=by)

    new_file_path = generate_random_file_name('spup', 'mp3')
    wavfile.write(f"{TEMP_FOLDER}/{new_file_path}", fs, song_2_times_faster)

    return new_file_path
