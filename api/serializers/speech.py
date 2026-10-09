from rest_framework import serializers

class SpeechToTextSerializer(serializers.Serializer):
    audio = serializers.FileField(required=True)
