'''from rest_framework import serializers

class TTSSerializer(serializers.Serializer):
    text = serializers.CharField()
    language = serializers.CharField(default="en")
    voice = serializers.CharField(default="female")
    speed = serializers.FloatField(default=1.0)
    pitch = serializers.IntegerField(default=0)'''
from rest_framework import serializers

class TextToSpeechSerializer(serializers.Serializer):
    text = serializers.CharField()
    voice = serializers.CharField(required=False, default="alloy")
