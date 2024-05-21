from google.cloud import texttospeech

from media.tts.tts import TTS

class GCloud(TTS):
    name = 'Google Cloud TTS'
    website = 'https://cloud.google.com/text-to-speech'
    supported_langs = ("pt-br", "en-us")
    supports_native_speed = True

    def translate_language_code(self, lang: str):
        return {
            'pt-br': 'pt-BR-Wavenet-B',
            'en-us': 'en-US-Neural2-J',
            'en': 'en-US-Neural2-J',
        }[lang.lower()]

    def generate(self, text: str, lang: str, speed: float=1) -> bytes:    
        # Instantiates a client
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code=lang, name=self.translate_language_code(lang), ssml_gender=texttospeech.SsmlVoiceGender.MALE
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speed
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        return response.audio_content