
from __future__ import annotations

import logging
from openai import OpenAI
from django.conf import settings
import os
import uuid

logger = logging.getLogger(__name__)


class TTSProviderError(Exception):
    """Raised when TTS provider fails."""
    pass


class OpenAITTS:
    """
    OpenAI Text-to-Speech provider.
    Returns raw audio bytes only.
    """

    def __init__(self) -> None:
        if not settings.OPENAI_API_KEY:
            raise TTSProviderError("OPENAI_API_KEY is not configured.")

        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def synthesize(self, text: str, voice: str = "alloy") -> bytes:
        if not text or not text.strip():
            raise TTSProviderError("Text must be non-empty.")

        try:
            response = self.client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice=voice,
                input=text,
            )

            # Recommended for OpenAI 2.x
            audio_bytes = response.read()

        except Exception as exc:
            logger.error(f"OpenAI TTS error: {str(exc)}")
            raise TTSProviderError("OpenAI TTS request failed.") from exc

        if not audio_bytes:
            raise TTSProviderError("OpenAI returned empty audio.")

        return audio_bytes


# High-level helper used by pipeline

   
'''
def generate_tts_bytes(text: str, voice: str = "alloy") -> str:
    provider = OpenAITTS()
    audio_bytes = provider.synthesize(text=text, voice=voice)

    # Create tts directory if not exists
    tts_dir = os.path.join(settings.MEDIA_ROOT, "tts")
    os.makedirs(tts_dir, exist_ok=True)

    # Unique filename
    filename = f"{uuid.uuid4()}.mp3"
    file_path = os.path.join(tts_dir, filename)

    # Save file
    with open(file_path, "wb") as f:
        f.write(audio_bytes)

    # Return relative media path
    return f"/media/tts/{filename}"
'''




def generate_tts_bytes(text: str, voice: str = "alloy") -> bytes:
    provider = OpenAITTS()
    audio_bytes = provider.synthesize(text=text, voice=voice)

    if not isinstance(audio_bytes, bytes):
        raise ValueError("TTS provider did not return bytes")

    return audio_bytes










