from datetime import datetime
from datetime import timedelta
from typing import Optional

import jwt

from . import settings
from app.exceptions.client_exceptions import Unauthorized
# from fastapi.security import OAuth2PasswordBearer

# Definimos una clase para manejar todo lo relacionado con JWT


class JWTManager:
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.expires_delta = timedelta(
            minutes=settings.JWT_EXPIRATION_TIME_MINUTES)
        # self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

    # Función para generar un token JWT
    def encode(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + self.expires_delta

        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(
            to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key,
                                 algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise Unauthorized(message='Token has expired')
        except jwt.InvalidSignatureError:
            raise Unauthorized(message='Token signature is invalid')
        except jwt.InvalidTokenError:
            raise Unauthorized(message='Token is invalid')

    # def get_token_from_header(self, auth_header: str):
    #     if not auth_header:
    #         raise Unauthorized(message='Authorization header is missing')
    #     scheme, token = auth_header.split()
    #     if scheme.lower() != 'bearer':
    #         raise Unauthorized(message='Invalid authentication scheme')
    #     return token


# Instance
jwt_manager = JWTManager()
