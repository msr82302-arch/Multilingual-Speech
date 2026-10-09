#heres the logic of realtime speec
import tempfile
from api.common.pipeline import SpeechToSpeechPipeline


class RealtimeSpeechPipeline:

    def __init__(self):
        self.pipeline = SpeechToSpeechPipeline()

    def process_chunk(self, audio_file, source_lang, target_lang):

        # Save temporary audio chunk
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
            for chunk in audio_file.chunks():
                temp_audio.write(chunk)

            temp_path = temp_audio.name

        # Run existing pipeline
        result = self.pipeline.run(
            text=None,
            audio_file=temp_path,
            source_language=source_lang,
            target_language=target_lang
        )

        return result