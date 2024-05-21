from utilities.types.languages import SupportedLanguages
from deep_translator import GoogleTranslator

class Translator:
    def __init__(self, from_: SupportedLanguages, to: SupportedLanguages):
        self.from_ = self._normalize_translator_lang(from_)
        self.to = self._normalize_translator_lang(to)

    def _normalize_translator_lang(self, lang: str):
        return lang.split("-")[0]
    
    def translate(self, text: str):
        if self.from_ == self.to:
            return text
                
        if self.to == 'pt':
            if text.lower() == 'showerthoughts': return "Pensamentos de banho"
            if text.lower() == 'askreddit': return "Pergunte ao reddit"
        
        
        return GoogleTranslator(self.from_, self.to).translate(text)