


from django.db import models
from django.contrib.auth.models import User


class TranslationHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    source_text = models.TextField()
    translated_text = models.TextField()

    source_language = models.CharField(max_length=20)
    target_language = models.CharField(max_length=20)

    audio_file = models.FileField(upload_to="translations/audio/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.source_language} → {self.target_language}"