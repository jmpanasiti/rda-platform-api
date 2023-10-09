from typing import List
from uuid import UUID

from fastapi import UploadFile
from fastapi.responses import FileResponse

from app.exceptions.base_http_exception import BaseHTTPException
from app.schemas.operations_schemas import OperationsRequestReq
from app.schemas.operations_schemas import OperationsRequestRes
from app.schemas.operations_schemas import OperationsRequestUpdateReq
from app.schemas.operations_schemas import OperationsSinisterReq
from app.schemas.operations_schemas import OperationsSinisterRes
from app.schemas.operations_schemas import OperationsSinisterUpdateReq
from app.service.operations_service import OperationsService


class OperationsController():
    def __init__(self) -> None:
        self.__operations_service = None

    @property
    def operations_service(self) -> OperationsService:
        if self.__operations_service is None:
            self.__operations_service = OperationsService()
        return self.__operations_service

    def get_requests_paginated(self, branch_id: UUID, limit: int, offset: int) -> List[OperationsRequestRes]:
        requests = self.operations_service.get_branch_requests(
            branch_id, limit, offset)
        return requests

    def get_request_by_id(self, branch_id: UUID, request_id: UUID) -> OperationsRequestRes:
        return self.operations_service.get_request_by_id(branch_id, request_id)

    def add_new_request(self, branch_id: UUID, request_data: OperationsRequestReq):
        return self.operations_service.add_new_request(branch_id, request_data)

    def approve_request(self, branch_id: UUID, request_id: UUID, approver_user_id: UUID):
        return self.operations_service.approve_request(branch_id, request_id, approver_user_id)

    def update_request(self, branch_id: UUID, request_id: UUID, request_data: OperationsRequestUpdateReq) -> OperationsRequestRes:
        return self.operations_service.update_request(branch_id, request_id, request_data)

    def delete_request(self, branch_id: UUID, request_id: UUID) -> None:
        return self.operations_service.delete_request(branch_id, request_id)

    async def upload_request_file(self, branch_id, request_id: UUID, file: UploadFile):
        try:
            content_file = await file.read()
            file_name = file.filename
            self.operations_service.upload_request_file(
                branch_id, content_file, file_name, request_id)
        except BaseHTTPException as ex:
            raise ex

    def download_request_file(self, branch_id: UUID, request_id: UUID, file_name: str):
        try:
            file_path = self.operations_service.get_request_download_path(
                branch_id, request_id, file_name)
            return FileResponse(file_path)
        except BaseHTTPException as ex:
            raise ex

    def delete_request_file(self, branch_id: UUID, request_id: UUID, file_name: str):
        try:
            self.operations_service.delete_request_file(
                branch_id, request_id, file_name)
        except BaseHTTPException as ex:
            raise ex

    def get_sinisters_paginated(self, branch_id: UUID, limit: int, offset: int) -> List[OperationsSinisterRes]:
        sinisters = self.operations_service.get_branch_sinisters(
            branch_id, limit, offset)
        return sinisters

    def get_sinister_by_id(self, branch_id: UUID, sinister_id: UUID) -> OperationsSinisterRes:
        return self.operations_service.get_sinister_by_id(branch_id, sinister_id)

    def add_new_sinister(self, branch_id: UUID, sinister_data: OperationsSinisterReq):
        return self.operations_service.add_new_sinister(branch_id, sinister_data)

    def approve_sinister(self, branch_id: UUID, sinister_id: UUID, approver_user_id: UUID):
        return self.operations_service.approve_sinister(branch_id, sinister_id, approver_user_id)

    def update_sinister(self, branch_id: UUID, sinister_id: UUID,
                        sinister_data: OperationsSinisterUpdateReq) -> OperationsSinisterRes:
        return self.operations_service.update_sinister(branch_id, sinister_id, sinister_data)

    def delete_sinister(self, branch_id: UUID, sinister_id: UUID) -> None:
        return self.operations_service.delete_sinister(branch_id, sinister_id)

    async def upload_sinister_file(self, branch_id, sinister_id: UUID, file: UploadFile):
        try:
            content_file = await file.read()
            file_name = file.filename
            self.operations_service.upload_sinister_file(
                branch_id, content_file, file_name, sinister_id)
        except BaseHTTPException as ex:
            raise ex

    def download_sinister_file(self, branch_id: UUID, sinister_id: UUID, file_name: str):
        try:
            file_path = self.operations_service.get_sinister_download_path(
                branch_id, sinister_id, file_name)
            return FileResponse(file_path)
        except BaseHTTPException as ex:
            raise ex

    def delete_sinister_file(self, branch_id: UUID, sinister_id: UUID, file_name: str):
        try:
            self.operations_service.delete_sinister_file(
                branch_id, sinister_id, file_name)
        except BaseHTTPException as ex:
            raise ex
