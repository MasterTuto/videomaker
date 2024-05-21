from abc import ABC, abstractmethod, abstractproperty

from utilities.types.languages import SupportedLanguages

class TTS(ABC):
    name: str
    website: str
    supported_langs: tuple[SupportedLanguages, ...]
    supports_native_speed: bool

    @abstractmethod
    def generate(self, text: str, lang: str, speed: float) -> bytes: ...

    def __str__(self):
        return self.name