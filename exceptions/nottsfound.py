class NoTTSFoundException(Exception):
    def __init__(self, lang: str) -> None:
        super().__init__(f"No TTS system encountered for lang: {lang}")