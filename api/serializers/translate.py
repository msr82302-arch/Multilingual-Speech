'''from rest_framework import serializers

class TranslateSerializer(serializers.Serializer):
    text = serializers.CharField(required=False, allow_blank=True)
    audio = serializers.FileField(required=False)
    target_lang = serializers.CharField(required=True)

    def validate(self, data):
        if not data.get("text") and not data.get("audio"):
            raise serializers.ValidationError(
                "Either text or audio file is required."
            )
        return data
'''
from rest_framework import serializers

class TranslateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True)
    target_lang = serializers.CharField(required=True)
    source_lang = serializers.CharField(required=False, default="auto")
















'''from rest_framework import serializers

class TranslateSerializer(serializers.Serializer):
    text = serializers.CharField()
    source_lang = serializers.CharField(required=False, default="auto")
    target_lang = serializers.CharField()'''
