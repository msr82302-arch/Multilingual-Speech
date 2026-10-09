
from rest_framework import serializers


class ProcessSerializer(serializers.Serializer):
    """
    Serializer for the unified /api/process/ endpoint.
    Accepts either text or audio (or both) plus a required target language.
    """

    text = serializers.CharField(required=False, allow_blank=True)
    audio = serializers.FileField(required=False)
    target_lang = serializers.CharField(required=True)
    source_lang = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        text = attrs.get("text")
        audio = attrs.get("audio")

        if (not text or not text.strip()) and audio is None:
            raise serializers.ValidationError(
                "Either non-empty text or an audio file must be provided."
            )

        return attrs





















'''

import logging

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.common.mongo_service import save_translation
from api.serializers.process_serializers import ProcessSerializers

from api.common.pipeline import SpeechToSpeechPipeline


logger = logging.getLogger(__name__)


class ProcessAPIView(APIView):
    """
    POST /api/process/

    Unified endpoint that accepts either text or audio and runs the
    SpeechToSpeechPipeline to produce translated text and synthesized audio.
    """

    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        In development, when DEBUG_PROCESS_API is True, allow unauthenticated
        access for easier testing. In production, require authentication.
        """
        if getattr(settings, "DEBUG_PROCESS_API", False):
            return [AllowAny()]
        return super().get_permissions()

    def post(self, request, *args, **kwargs):

        serializer = ProcessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data

        text = validated.get("text")
        audio_file = validated.get("audio")
        target_lang = validated["target_lang"]
        source_lang = validated.get("source_lang") or None

        # 🔒 Billing Protection: Ensure at least one valid input
        if (not text or not str(text).strip()) and not audio_file:
            return Response(
                {"detail": "Either non-empty text or an audio file is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 🔒 Billing Protection: Limit text length
        if text and len(text) > 1000:
            return Response(
                {"detail": "Text too long. Maximum 1000 characters allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        pipeline = SpeechToSpeechPipeline()

        try:
            logger.info(f"Pipeline started for user {request.user.id}")

            result = pipeline.run(
                text=text,
                audio_file=audio_file,
                source_language=source_lang,
                target_language=target_lang,
            )

            translated_text = result.get("translated_text")

            # ✅ Save using user ID (professional practice)
            save_translation(
                user_id=request.user.id,
                original_text=text,
                translated_text=translated_text,
                source_lang=source_lang,
                target_lang=target_lang,
            )

            logger.info(f"Pipeline completed for user {request.user.id}")

            return Response(result, status=status.HTTP_200_OK)

        except ValueError as e:
            logger.warning(f"Validation error: {str(e)}")
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.error(f"Processing failed: {str(e)}")
            return Response(
                {
                    "detail": "Processing failed.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )




from rest_framework import serializers



def post(self, request, *args, **kwargs):
    serializer = ProcessSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    validated = serializer.validated_data

    text = validated.get("text")
    audio_file = validated.get("audio")
    target_lang = validated["target_lang"]
    source_lang = validated.get("source_lang") or None

    # 🔒 Billing Protection: Ensure at least one input
    if not text and not audio_file:
        return Response(
            {"detail": "Either text or audio is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 🔒 Billing Protection: Limit text size
    if text and len(text) > 1000:
        return Response(
            {"detail": "Text too long. Maximum 1000 characters allowed."},
            status=status.HTTP_400_BAD_REQUEST
        )

    pipeline = SpeechToSpeechPipeline()

    try:
        logger.info(f"Pipeline started for user {request.user.id}")

        result = pipeline.run(
            text=text,
            audio_file=audio_file,
            source_language=source_lang,
            target_language=target_lang,
        )

        translated_text = result.get("translated_text")

        # ✅ Use user ID safely
        save_translation(
            user_id=request.user.id,
            original_text=text,
            translated_text=translated_text,
            source_lang=source_lang,
            target_lang=target_lang
        )

        logger.info(f"Pipeline completed for user {request.user.id}")

        return Response(result, status=status.HTTP_200_OK)

    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        return Response(
            {"detail": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        return Response(
            {
                "detail": "Processing failed.",
                "error": str(e),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


















from rest_framework import serializers


class ProcessSerializer(serializers.Serializer):
    """
    Serializer for the unified /api/process/ endpoint.
    Accepts either text or audio (or both) plus a required target language.
    """


    text = serializers.CharField(required=False, allow_blank=True)
    audio = serializers.FileField(required=False)
    target_lang = serializers.CharField(required=True)
    source_lang = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        text = attrs.get("text")
        audio = attrs.get("audio")

        if (not text or not text.strip()) and audio is None:
            raise serializers.ValidationError(
                "Either non-empty text or an audio file must be provided."
            )

        return attrs'''

