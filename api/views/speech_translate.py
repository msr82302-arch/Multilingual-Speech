from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from api.serializers.speech_translate import SpeechTranslateSerializer
from api.services.speech.whisper_service import transcribe_audio
from api.services.translate.translate_service import translate_text


class SpeechTranslateAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = SpeechTranslateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        audio = serializer.validated_data["audio"]
        target_lang = serializer.validated_data["target_lang"]
        source_lang = serializer.validated_data.get("source_lang", "auto")

        text = transcribe_audio(audio)
        translated = translate_text(
            text=text,
            target_lang=target_lang,
            source_lang=source_lang
        )

        return Response({
            "transcription": text,
            "translated_text": translated,
            "target_lang": target_lang
        }, status=status.HTTP_200_OK)
