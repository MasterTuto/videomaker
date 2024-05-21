import json
import urllib.parse

import requests

from media.tts.tts import TTS


class TTSMP3(TTS):
    name = "TTSMP3"
    website = "https://ttsmp3.com/"
    multiplier = 1.2
    supports_native_speed = False

    supported_langs = ("pt-br", "en-us", "en")

    def translate_lang_id(self, lang: str):
        language_translator = {
            "ar": "Zeina",
            "en-au": "Russell",
            "pt-br": "Ricardo",
            "en-us": "Matthew",
        }

        return language_translator[lang.lower()]

    def generate(self, text: str, lang: str, _: float) -> bytes:
        text = urllib.parse.quote(text)
        lang = self.translate_lang_id(lang)

        getter_url = "https://ttsmp3.com/makemp3_new.php"
        payload = f"msg={text}&lang={lang}&source=ttsmp3"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-type": "application/x-www-form-urlencoded",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Referrer": "https://ttsmp3.com/",
        }

        res = requests.post(
            getter_url,
            data=payload,
            headers=headers
        )
        
        audio_json = json.loads(res.text)
        audio_url = audio_json['URL']
        content = requests.get(audio_url).content

        return content
