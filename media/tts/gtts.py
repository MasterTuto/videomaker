import gtts
from media.tts.tts import TTS

class gTTS(TTS):
    name = "gTTS"
    website = "https://translate.google.com/"
    multiplier = 1.2
    supports_native_speed = False

    supported_langs = ("pt-br", "en-us")

    def generate(self, text: str, lang: str, _: float) -> bytes:
        x = gtts.gTTS(
            text=text,
            lang=lang,
            slow=False,
        )

        return bytes().join(x.stream())
