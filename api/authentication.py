from rest_framework.exceptions import AuthenticationFailed
from api.auth.firebase import *   
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.contrib.auth.models import User
from firebase_admin import auth
import firebase_admin

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        try:
            id_token = auth_header.split("Bearer ")[1]
        except IndexError:
            raise exceptions.AuthenticationFailed("Invalid token header")

        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise exceptions.AuthenticationFailed("Invalid Firebase token")

        uid = decoded_token.get("uid")
        email = decoded_token.get("email")

        if not uid:
            raise exceptions.AuthenticationFailed("Invalid token payload")

        user, created = User.objects.get_or_create(
            username=uid,
            defaults={"email": email}
        )

        return (user, None)