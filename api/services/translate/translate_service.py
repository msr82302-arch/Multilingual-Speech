
from deep_translator import GoogleTranslator

def translate_text(text, target_lang, source_lang="auto"):
    translator = GoogleTranslator(
        source=source_lang,
        target=target_lang
    )
    return translator.translate(text)
