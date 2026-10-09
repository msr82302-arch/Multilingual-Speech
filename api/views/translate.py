from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from api.serializers.translate import TranslateSerializer
from api.services.translate.translate_service import translate_text


class TranslateAPIView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = TranslateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        text = serializer.validated_data["text"]
        target_lang = serializer.validated_data["target_lang"]
        source_lang = serializer.validated_data.get("source_lang", "auto")

        translated = translate_text(
            text=text,
            target_lang=target_lang,
            source_lang=source_lang
        )

        return Response({
            "original_text": text,
            "translated_text": translated,
            "target_lang": target_lang
        })


















'''from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from api.serializers.translate import TranslateSerializer
from api.services.speech.whisper_service import transcribe_audio
from api.services.translate.translate_service import translate_text


class TranslateAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer)

    def get(self, request):
        """
        Only to render fields in DRF UI
        """
        serializer = TranslateSerializer()
        return Response(serializer.data)

    def post(self, request):
        serializer = TranslateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        text = serializer.validated_data.get("text")
        audio = serializer.validated_data.get("audio")
        target_lang = serializer.validated_data["target_lang"]

        if audio:
            text = transcribe_audio(audio)

        translated_text = translate_text(text, target_lang)

        return Response({
            "original_text": text,
            "translated_text": translated_text,
            "target_lang": target_lang
        })

'''

'''from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers.translate import TranslateSerializer
from api.services.translate.translate_service import translate_text

class TranslateAPIView(APIView):
    def post(self, request):
        serializer = TranslateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        translated = translate_text(
            text=serializer.validated_data["text"],
            target_lang=serializer.validated_data["target_lang"],
            source_lang=serializer.validated_data.get("source_lang", "auto")
        )

        return Response({
            "original_text": serializer.validated_data["text"],
            "translated_text": translated
        }, status=status.HTTP_200_OK)
'''