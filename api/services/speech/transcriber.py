from faster_whisper import WhisperModel
import os

# Load model once (production safe)
model = WhisperModel(
    "base",
    device="cpu",       # safe for your DDR3 RAM
    compute_type="int8" # low memory usage
)

def speech_to_text(audio_path: str) -> str:
    """
    Convert speech audio file to text
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError("Audio file not found")

    segments, _ = model.transcribe(audio_path)

    text_output = []
    for segment in segments:
        text_output.append(segment.text)

    return " ".join(text_output).strip()
