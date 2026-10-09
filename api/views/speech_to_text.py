from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api.serializers.speech import SpeechToTextSerializer
from api.services.speech.whisper_service import transcribe_audio


class SpeechToTextView(GenericAPIView):
    serializer_class = SpeechToTextSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            audio_file = serializer.validated_data["audio"]
            text = transcribe_audio(audio_file)

            return Response(
                {"text": text},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






















'''
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from api.serializers.speech import SpeechToTextSerializer
from api.services.speech.whisper import transcribe_audio


class SpeechToTextView(CreateAPIView):
    serializer_class = SpeechToTextSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        audio_file = serializer.validated_data["audio"]
        text = transcribe_audio(audio_file)

        return Response(
            {"text": text},
            status=status.HTTP_200_OK
        )























from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.conf import settings
import os
import uuid

from api.services.speech.transcriber import speech_to_text


class SpeechToTextView(APIView):
    """
    Upload audio file and return transcribed text
    """

    def post(self, request):
        audio_file = request.FILES.get("audio")

        if not audio_file:
            return Response(
                {"error": "Audio file is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save file
        filename = f"{uuid.uuid4()}_{audio_file.name}"
        file_path = default_storage.save(
            f"audio/{filename}", audio_file
        )

        full_path = os.path.join(settings.MEDIA_ROOT, file_path)

        try:
            text = speech_to_text(full_path)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                "text": text,
                "file": file_path
            },
            status=status.HTTP_200_OK
        )









er = SpeechToTextSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        audio_file = serializer.validated_data["audio"]

        filename = f"{uuid.uuid4()}_{audio_file.name}"
        file_path = os.path.join(settings.MEDIA_ROOT, "uploads", filename)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb+") as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

        result = speech_to_text(file_path)

        os.remove(file_path)  # IMPORTANT (no storage leak)

        return Response(result)
'''