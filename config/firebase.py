'''import firebase_admin
from firebase_admin import credentials

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

cred_path = os.path.join(BASE_DIR,'speech-translate-app-bd85b-firebase-adminsdk-fbsvc-ebec003906.json' )

cred = credentials.Certificate(cred_path)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)'''


##'firebase_service_account.json