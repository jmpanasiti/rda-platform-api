import logging

from app.core.jwt import jwt_manager
from app.exceptions import server_exceptions as se
from app.exceptions.base_http_exception import BaseHTTPException
from app.schemas.auth_schemas import LoginSchema
from app.schemas.auth_schemas import RegisterSchema
from app.schemas.auth_schemas import TokenResponse
from app.schemas.token_schemas import DecodedJWT
from app.service.auth_service import AuthService
from app.service.user_service import UserService

logger = logging.getLogger(__name__)


class AuthController():
    def __init__(self) -> None:
        self.__user_service = None
        self.__auth_service = None

    @property
    def user_service(self) -> UserService:
        if self.__user_service is None:
            self.__user_service = UserService()
        return self.__user_service

    @property
    def auth_service(self) -> AuthService:
        if self.__auth_service is None:
            self.__auth_service = AuthService()
        return self.__auth_service

    def register(self, register_data: RegisterSchema) -> TokenResponse:
        try:
            token = self.auth_service.register(register_data)
            return TokenResponse(access_token=token)
        except BaseHTTPException as ex:
            raise ex

    def login(self, credentials: LoginSchema) -> TokenResponse:
        try:
            token = self.auth_service.login(credentials)
            return TokenResponse(access_token=token)
        except BaseHTTPException as ex:
            raise ex

    def get_current_user_info(self, token: DecodedJWT):
        try:
            return self.user_service.get_by_id(token.id)
        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.critical(f'Unhandled error: {"; ".join(ex.args)}')
            raise se.InternalServerError(
                'Something went wrong getting user info. Please contact the sysadmin')

    def renew_token(self, token: DecodedJWT) -> TokenResponse:
        payload = {
            'id': str(token.id),
            'role': token.role,
        }
        new_token = jwt_manager.encode(payload)

        return TokenResponse(access_token=new_token)
