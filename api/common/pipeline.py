from __future__ import annotations

import uuid
import logging
from pathlib import Path
from typing import Optional, Dict, Any

from django.conf import settings
from pydub import AudioSegment
from openai import OpenAI

from api.services.translate.translate_service import translate_text
from api.services.tts.openai_tts_service import generate_tts_bytes
import os

logger = logging.getLogger(__name__)
client = OpenAI()


class SpeechToSpeechPipeline:
    """
    Unified Speech-to-Speech Pipeline

    Flow:
    1. Accept text OR audio
    2. If audio → convert + transcribe using Whisper
    3. Translate text
    4. Generate TTS
    5. Save output audio
    6. Return structured result
    """

    def run(
        self,
        *,
        target_language: str,
        text: Optional[str] = None,
        audio_file: Optional[Any] = None,
        source_language: Optional[str] = None,
    ) -> Dict[str, Any]:

        if not target_language:
            raise ValueError("Target language is required.")

        original_text: Optional[str] = None

        # =====================================================
        # 1️⃣ HANDLE TEXT INPUT
        # =====================================================
        if text and text.strip():
            original_text = text.strip()

        # =====================================================
        # 2️⃣ HANDLE AUDIO INPUT (REAL STT IMPLEMENTATION)
        # =====================================================
        elif audio_file:

            try:
                media_root = Path(settings.MEDIA_ROOT)
                upload_dir = media_root / "uploads"
                upload_dir.mkdir(parents=True, exist_ok=True)

                # Unique filename
                # unique_input_name = f"{uuid.uuid4()}_{audio_file.name}"
                if isinstance(audio_file, str):
                    file_name = os.path.basename(audio_file)
                else:
                    file_name = audio_file.name

                unique_input_name = f"{uuid.uuid4()}_{file_name}"
                temp_path = upload_dir / unique_input_name
                '''
                # Save uploaded file
                with open(temp_path, "wb") as f:
                    for chunk in audio_file.chunks():
                        f.write(chunk)'''
                                # Save uploaded file
                if isinstance(audio_file, str):
                    temp_path = Path(audio_file)

                else:
                    unique_input_name = f"{uuid.uuid4()}_{audio_file.name}"
                    temp_path = upload_dir / unique_input_name

                    with open(temp_path, "wb") as f:
                        for chunk in audio_file.chunks():
                            f.write(chunk)

                # Convert to WAV
                wav_path = temp_path.with_suffix(".wav")
                audio = AudioSegment.from_file(temp_path)
                audio.export(wav_path, format="wav")

                # ===== Whisper STT =====
                with open(wav_path, "rb") as audio_data:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_data
                    )

                original_text = transcript.text

                logger.info(f"Recognized text: {original_text}")

                # Clean temp files
                if temp_path.exists():
                    temp_path.unlink()
                if wav_path.exists():
                    wav_path.unlink()

            
            #except Exception as e:
            #   logger.error(f"Audio processing failed: {str(e)}")
            #    raise ValueError(f"Audio processing failed: {str(e)}")'''
            except Exception as e:
                import traceback
                traceback.print_exc()
                raise ValueError(f"Audio processing failed: {str(e)}")
        else:
            raise ValueError("Text or audio input required.")

        #if not original_text:
         #   raise ValueError("Speech recognition returned empty result.")
        if not original_text or len(original_text.split()) < 2:
            raise ValueError("Audio does not contain valid speech.")
        logger.info("Pipeline started")

        # =====================================================
        # 3️⃣ TRANSLATION
        # =====================================================
        translated_text = original_text

        try:
            if not source_language or source_language.lower() == "auto":
                effective_source = None
            else:
                effective_source = source_language

            if not effective_source or effective_source != target_language:
                translated_text = translate_text(
                    text=original_text,
                    target_lang=target_language,
                    source_lang=effective_source,
                )

        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            raise ValueError("Translation service failed.")

        if not translated_text:
            raise ValueError("Translation returned empty result.")

        # =====================================================
        # 4️⃣ TEXT TO SPEECH
        # =====================================================
        try:
            audio_bytes = generate_tts_bytes(
                text=translated_text,
                voice="alloy",
            )
        except Exception as e:
            logger.error(f"TTS generation failed: {str(e)}")
            raise ValueError("Text-to-speech generation failed.")

        if not audio_bytes:
            raise ValueError("No audio data returned from TTS.")

        # =====================================================
        # 5️⃣ SAVE OUTPUT AUDIO
        # =====================================================
        try:
            media_root = Path(settings.MEDIA_ROOT)
            output_dir = media_root / "tts_outputs"
            output_dir.mkdir(parents=True, exist_ok=True)

            filename = f"{uuid.uuid4()}.mp3"
            output_path = output_dir / filename

            with open(output_path, "wb") as f:
                f.write(audio_bytes)

        except Exception as e:
            raise Exception(f"Audio saving failed: {e}")

        audio_url = f"{settings.MEDIA_URL}tts_outputs/{filename}"

        logger.info(f"File saved successfully: {output_path}")

        return {
            "original_text": original_text,
            "translated_text": translated_text,
            "audio_url": audio_url,
        }