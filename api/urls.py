from django.urls import path
from api.views.speech_to_text import SpeechToTextView
from api.views.translate import TranslateAPIView
from api.views.speech_translate import SpeechTranslateAPIView
from api.views.tts import TextToSpeechAPIView
#from api.views.process import ProcessSerializer
from api.views.process import ProcessAPIView
from api.views.process import RealTimeProcessAPIView
#from api.views.signup import SignupAPIView
#from .views import auth_views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path("speech-to-text/", SpeechToTextView.as_view(), name="speech-to-text"),
    path("translate/", TranslateAPIView.as_view()),
    path("speech-translate/", SpeechTranslateAPIView.as_view()),
    path("tts/", TextToSpeechAPIView.as_view()),
    path("process/", ProcessAPIView.as_view()),
    path("realtime-process/", RealTimeProcessAPIView.as_view()),
    #path("signup/",signup)
   
    #path('token/refresh/', TokenRefreshView.as_view()),
   # path("signup/", auth_views.signup_view, name="signup"),
    #path("login/", auth_views.login_view, name="login"),
    #path("logout/", auth_views.logout_view, name="logout"),
    

]




'''
{
  "text": "Hello, this is production level TTS",
  "language": "en",
  "voice": "female",
  "speed": 1.0,
  "pitch": 0,
  "provider": "coqui"
}
'''
'''
        save_translation(
                user_id=str(request.user),
                original_text=original_text,
                translated_text=translated_text,
                source_lang=source_language,
                target_lang=target_language) 

            
         return Response(result, status=status.HTTP_200_OK)'''
            


















