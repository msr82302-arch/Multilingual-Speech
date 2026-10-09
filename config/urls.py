
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("web.urls")),      
    path("api/", include("api.urls")),
    #path('api/login/', TokenObtainPairView.as_view()),
    #path('api/token/refresh/', TokenRefreshView.as_view()),
    
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







'''
{
"text" : "hey tier is an apple at front of you",
"voice" : " alloy",
}
'''


'''
{
"text" : "hlo now i have to move on with new strategy!",
"source_lang" : "eng",
"target_lang" : "urdu"
}'''






"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

from django.contrib import admin
from django.urls import path,include
#from rest_framework.response import Response
#rom rest_framework.decorators import api_view
'''
@api_view(['GET'])
def test_api(request):
    return Response({"message": "Backend is connected 🎉"})'''


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path("api-auth/", include("rest_framework.urls")),
]
"""
