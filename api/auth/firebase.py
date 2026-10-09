import firebase_admin
from firebase_admin import credentials
from django.conf import settings
import os

# Prevent re-initialization
if not firebase_admin._apps:
    BASE_DIR = settings.BASE_DIR

    cred_path = os.path.join(
        BASE_DIR,
        "google-credentials.json"
    )

    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)