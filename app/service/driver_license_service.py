import os
from typing import List
from uuid import UUID

from ..database.models import DriverLicenseModel
from ..repository.driver_license_repository import DriverLicenseRepository as DriverLicenseRepo
from ..schemas.driver_license_schemas import DriverLicenseRequest as DriverLicenseReq
from ..schemas.driver_license_schemas import DriverLicenseResponse as DriverLicenseRes
from .base_service import BaseService
from .user_service import UserService


class DriverLicenseService(BaseService[DriverLicenseModel, DriverLicenseReq, DriverLicenseRes, DriverLicenseRepo]):
    folder_path: str = './files/driver_licenses'

    def __init__(self):
        super().__init__(DriverLicenseRepo)
        self.user_service = UserService()

    def upload(self, request_schema: DriverLicenseReq) -> DriverLicenseRes:
        try:
            current_licenses = self.get_by_user(request_schema.user_id)

            if len(current_licenses) == 0:  # Create
                response_schema = self.create(request_schema)

                with open(f'{self.folder_path}/{response_schema.id}_{response_schema.file_name}', 'wb') as file:
                    file.write(request_schema.content_file)
                return response_schema

            # Else, update
            current_license = current_licenses[-1]
            old_file_path = f'{self.folder_path}/{current_license.id}_{current_license.file_name}'

            current_license.file_name = request_schema.file_name
            current_license.file_type = request_schema.file_type

            response_schema = self.update(current_license.id, request_schema)

            # Delete old file
            os.remove(old_file_path)

            # Create new one
            with open(f'{self.folder_path}/{response_schema.id}_{response_schema.file_name}', 'wb') as file:
                file.write(request_schema.content_file)

            return response_schema
        except Exception as ex:
            raise ex

    def get_download_path(self, license_id: UUID) -> str:
        response_schema = self.get_by_id(license_id)
        return f'{self.folder_path}/{response_schema.id}_{response_schema.file_name}'

    def get_by_user(self, user_id: UUID) -> List[DriverLicenseRes]:
        search_filter = {
            'user_id': user_id
        }
        licenses = self.repo.get_list_by_filter(search_filter)
        return [self._to_schema(license_model) for license_model in licenses]

    def _to_schema(self, model: DriverLicenseModel | dict, *args) -> DriverLicenseRes:
        if type(model) is dict:
            return DriverLicenseRes(**model)
        return DriverLicenseRes(
            id=model.id,
            file_name=model.file_name,
            file_type=model.file_type,
            file_url='falta_url',
            created_at=model.created_at,
            updated_at=model.updated_at,
            expiration_date=model.expiration_date,
        )
