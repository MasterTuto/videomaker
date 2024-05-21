import logging

from media.tts.ttsmp3 import TTSMP3
from media.tts.gtts import gTTS
from media.tts.gcloud import GCloud
from media.tts.tts import TTS
from exceptions.nottsfound import NoTTSFoundException

ALL_TTS: list[TTS] = [
    GCloud(),
    TTSMP3(),
    gTTS(),
]

def generate_audio(text: str, lang: str, speed: float):
    ttslogger = logging.getLogger("tts")

    for tts in ALL_TTS:
        try:
            if lang.lower() in tts.supported_langs:
                ttslogger.info(f'Genenerating the text "%s" (lang: %s) on TTS %s', text, lang, tts.name)
                audio = tts.generate(text, lang, speed)
                return audio, tts.supports_native_speed
            else:
                ttslogger.warn(f'Lang "%s" not supported for TTS "%s"', lang, tts.name)
        except Exception as e:
            print(e)
            ttslogger.error(f"An error ocurred when tying {tts.name}")
            continue
    
    raise NoTTSFoundException(lang)