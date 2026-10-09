


import tempfile
import os

from faster_whisper import WhisperModel


def transcribe_audio(audio_file):
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        for chunk in audio_file.chunks():
            temp.write(chunk)
        temp_path = temp.name

    try:
        model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

        segments, info = model.transcribe(temp_path)

        text = " ".join([segment.text for segment in segments])
        return text.strip()

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)



























'''from faster_whisper import WhisperModel
import os
import uuid

MODEL_SIZE = "base"  # later: small / medium

model = WhisperModel(
    MODEL_SIZE,
    device="cpu",
    compute_type="int8"
)

def speech_to_text(audio_path: str) -> dict:
    segments, info = model.transcribe(audio_path)

    full_text = ""
    for segment in segments:
        full_text += segment.text + " "

    return {
        "text": full_text.strip(),
        "language": info.language,
        "duration": info.duration
    }
def transcribe_audio(audio_file):
    # TEMP test logic
    return "Audio received successfully"
'''