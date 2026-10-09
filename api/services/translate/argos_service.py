from .base import BaseTranslator
from argostranslate import translate

class ArgosTranslator(BaseTranslator):
    def translate(self, text, target_lang):
        return translate.translate(text, "en", target_lang)
