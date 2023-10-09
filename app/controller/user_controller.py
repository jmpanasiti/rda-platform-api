import logging
from datetime import date
from uuid import UUID

from fastapi import UploadFile
from fastapi.responses import FileResponse

from app.core.enums.role_enum import ADMIN_ROLES
from app.core.enums.role_enum import RoleEnum as Role
from app.exceptions import client_exceptions as ce
from app.exceptions.base_http_exception import BaseHTTPException
from app.schemas.driver_license_schemas import DriverLicenseRequest
from app.schemas.token_schemas import DecodedJWT
from app.schemas.user_schemas import FirstSuperAdmin
from app.schemas.user_schemas import UserRequest
from app.schemas.user_schemas import UserResponse
from app.schemas.user_schemas import UserUpdateRequest
from app.service.branch_service import BranchService
from app.service.driver_license_service import DriverLicenseService
from app.service.user_service import UserService

logger = logging.getLogger(__name__)


class UserController():
    def __init__(self) -> None:
        self.__user_service = None
        self.__branch_service = None
        self.__driver_license_service = None

    @property
    def user_service(self) -> UserService:
        if self.__user_service is None:
            self.__user_service = UserService()
        return self.__user_service

    @property
    def branch_service(self) -> BranchService:
        if self.__branch_service is None:
            self.__branch_service = BranchService()
        return self.branch_service

    @property
    def driver_license_service(self) -> DriverLicenseService:
        if self.__driver_license_service is None:
            self.__driver_license_service = DriverLicenseService()
        return self.__driver_license_service

    def create(self, user_request: UserRequest):
        try:
            if user_request.password is None:
                raise ce.BadRequest('Password can\'t be null on create')
            new_user = self.user_service.create(user_request)
            return new_user
        except BaseHTTPException as ex:
            raise ex

    def get_list(self, limit: int, offset: int):
        try:
            return self.user_service.get_all(limit, offset)
        except BaseHTTPException as ex:
            raise ex

    def get_by_id(self, user_id: UUID):
        try:
            return self.user_service.get_by_id(user_id)
        except BaseHTTPException as ex:
            raise ex

    def update(self, token: DecodedJWT,  user_id: UUID, user_data: UserUpdateRequest):
        try:
            if user_id != token.id and token.role not in ADMIN_ROLES:
                raise ce.Forbidden('You can\'t edit this user.')

            return self.user_service.update(user_id, user_data)
        except BaseHTTPException as ex:
            raise ex

    def delete(self, user_id: UUID):
        try:
            return self.user_service.delete(user_id)
        except BaseHTTPException as ex:
            raise ex

    def activate(self, user_id: UUID):
        try:
            return self.user_service.activate(user_id)
        except BaseHTTPException as ex:
            raise ex

    def deactivate(self, user_id: UUID):
        try:
            return self.user_service.deactivate(user_id)
        except BaseHTTPException as ex:
            raise ex

    def create_default_superadmin(self, admin_data: FirstSuperAdmin) -> UserResponse:
        try:
            superadmins = self.user_service.get_all(
                1, 0, {'role': Role.superadmin})
            if len(superadmins) > 0:
                raise ce.BadRequest(
                    'There are at least one user with superadmin role.')

            user_data = UserRequest(
                username=admin_data.username,
                email=admin_data.email,
                password=admin_data.password,
                role=Role.superadmin,
                first_name='super',
                last_name='admin',
            )
            return self.create(user_data)
        except BaseHTTPException as ex:
            raise ex

    # ! DRIVER LICENSE
    async def upload_license(self, user_id: UUID, expiration_date: date, file: UploadFile):
        try:
            content_file = await file.read()
            license_request = DriverLicenseRequest(
                expiration_date=expiration_date,
                content_file=content_file,
                file_name=file.filename,
                file_type=file.content_type,
                user_id=user_id,
            )
            response = self.driver_license_service.upload(license_request)
            return response
        except BaseHTTPException as ex:
            raise ex

    def download_license(self, license_id: UUID):
        try:
            file_path = self.driver_license_service.get_download_path(
                license_id)
            return FileResponse(file_path)
        except BaseHTTPException as ex:
            raise ex

    def get_license_data(self, license_id: UUID):
        try:
            return self.driver_license_service.get_by_id(license_id)
        except BaseHTTPException as ex:
            raise ex
