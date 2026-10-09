from rest_framework import serializers

class SpeechTranslateSerializer(serializers.Serializer):
    audio = serializers.FileField(required=True)
    target_lang = serializers.CharField(required=True)
    source_lang = serializers.CharField(required=False, default="auto")
