
import logging

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
#from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from api.serializers.auth_serializers import RegisterSerializer
from api.serializers.process_serializers import ProcessSerializer
from api.services.process_service import ProcessService
from api.throttles import ProcessRateThrottle
from api.models.professor import TranslationHistory
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsProfessor
import os
from pydub import AudioSegment
from django.conf import settings
from api.common.realtime_pipeline import RealtimeSpeechPipeline



logger = logging.getLogger(__name__)

#ermission_classes = [IsAuthenticated, IsProfessor]

class ProcessAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    def post(self, request, *args, **kwargs):

        print("FILES RECEIVED:", request.FILES)  # Debug

        serializer = ProcessSerializer(
            data=request.data   # ✅ ONLY this
        )

        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        service = ProcessService()
        result = service.run(validated_data, request.user)

        audio_url = result.get("audio_url")

        response_data = {
            "translated_text": result.get("translated_text"),
        }

        if audio_url:
            response_data["audio_url"] = request.build_absolute_uri(audio_url)

       # return Response(response_data, status=200)
    
        translation = TranslationHistory.objects.create(
            user=request.user,
            source_text=validated_data.get("text") or "",
            translated_text=result.get("translated_text"),
            source_language=validated_data.get("source_lang"),
            target_language=validated_data.get("target_lang"),
        )
        return Response(response_data, status=200)
        
class RealTimeProcessAPIView(APIView):

    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    pipeline = RealtimeSpeechPipeline()

    def post(self, request, *args, **kwargs):

        try:

            audio_chunk = request.FILES.get("audio")

            source_lang = request.data.get("source_lang")
            target_lang = request.data.get("target_lang")

            if not audio_chunk:
                return Response({"error": "Audio missing"}, status=400)

            result = self.pipeline.process_chunk(
                audio_chunk,
                source_lang,
                target_lang
            )

            return Response({
                "translated_text": result.get("translated_text"),
                "audio_url": result.get("audio_url")
            })

        except Exception as e:

            print("REALTIME ERROR:", e)

            return Response(
                {"error": str(e)},
                status=500
            )

        return Response(response_data, status=200)




























