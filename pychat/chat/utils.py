import base64
import datetime
from uuid import uuid4

from django.conf import settings
from django.core.files.base import ContentFile
import jwt

def base64_to_image(base64_string):
    format, imgstr = base64_string.split(';base64,')
    ext = format.split('/')[-1]
    return ContentFile(base64.b64decode(imgstr), name=uuid4().hex + "." + ext)

def generate_token(user):
    token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm='HS256')

    return token

def generate_refresh_token(user):
    refresh_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }

    refresh = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')

    return refresh