from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from passlib.handlers.django import django_pbkdf2_sha256

from configs.settings import settings


def hash_password(password: str):
    return django_pbkdf2_sha256.hash(password)


def verify_password(password, encrypted_pasword):
    return django_pbkdf2_sha256.verify(password, encrypted_pasword)


def create_access_token(data: dict, expires_delta: Optional[timedelta]):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
