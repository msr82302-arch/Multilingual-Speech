

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers.tts import TextToSpeechSerializer

from api.services.tts.openai_tts_service import generate_tts_bytes


#permission_classes = [AllowAny]

class TextToSpeechAPIView(APIView):
    def post(self, request):
        serializer = TextToSpeechSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        
        audio_path = generate_tts(
            text=serializer.validated_data["text"],
            voice=serializer.validated_data.get("voice", "alloy"),
        )

        if audio_path:
            audio_url = request.build_absolute_uri(audio_path)
        else:
            audio_url = None

        return Response(
            {
                "success": True,
                "audio_url": audio_url
            },
            status=status.HTTP_201_CREATED
        )



































'''from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.tts.engine import TTSEngine
#from .coqui_service import CoquiTTS

class TextToSpeechAPIView(APIView):

    def post(self, request):
        text = request.data.get("text")
        language = request.data.get("language", "en")
        voice = request.data.get("voice", "female")
        speed = float(request.data.get("speed", 1.0))
        pitch = int(request.data.get("pitch", 0))
        provider = request.data.get("provider", "coqui")

        if not text  or not text.strip():
            return Response(
                {"error": "text is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:

            engine = TTSEngine(provider=provider)

            audio_path = engine.synthesize(
               text=text,
               language=language,
               voice=voice,
               speed=speed,
               pitch=pitch
        )

        except ValueError as e:
            return Rsponse( 
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print("TTS API ERROR:",e)
            return Response(
                {
                    "error":"Text-to-speec failed!",
                    "details":str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVICE_ERROR
            )

        return Response(
            {
                "status":"success",
                "audio_path": audio_path,
                "provider": provider,
                "language": language,
                "voice": voice
                #"speed": speed,
                #"pitch":pitch
            },
            status=status.HTTP_200_OK
        )
'''