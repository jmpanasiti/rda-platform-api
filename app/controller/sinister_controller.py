import logging
from typing import List
from uuid import UUID

from fastapi import UploadFile
from fastapi.responses import FileResponse

from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.exceptions.base_http_exception import BaseHTTPException
from app.schemas.sinister_schemas import SinisterRequest
from app.schemas.sinister_schemas import SinisterResponse
from app.service.sinister_service import SinisterService

logger = logging.getLogger(__name__)


class SinisterController():
    def __init__(self) -> None:
        self.__sinister_service = None

    @property
    def sinister_service(self) -> SinisterService:
        if self.__sinister_service is None:
            self.__sinister_service = SinisterService()
        return self.__sinister_service

    def create(self, sinister: SinisterRequest) -> SinisterResponse:
        try:
            new_sinister = self.sinister_service.create(sinister)
            return new_sinister
        except ce.BadRequest as ex:
            raise ex
        except Exception as ex:
            logger.critical("Not handled error")
            logger.error('; '.join(ex.args))
            raise se.InternalServerError(
                'Something went wrong, contact the admin')

    def get_list_paginated(self, limit: int, offset: int) -> List[SinisterResponse]:
        try:
            response = self.sinister_service.get_all(limit, offset)
            return response
        except Exception as ex:
            logger.critical(f'Unhandled error: {"; ".join(ex.args)}')
            raise se.InternalServerError(
                'Something went wrong on listing orgs. Please contact the sysadmin')

    def get_by_id(self, sinister_id: UUID):
        try:
            response = self.sinister_service.get_by_id(sinister_id)
            return response
        except ce.NotFound as ex:
            raise ex

    def update(self, sinister_id: UUID, sinister_data: SinisterRequest) -> SinisterResponse:
        try:
            response = self.sinister_service.update(sinister_id, sinister_data)
            return response
        except ce.NotFound as ex:
            raise ex

    def delete(self, sinister_id: UUID):
        try:
            self.sinister_service.delete(sinister_id)
        except ce.NotFound as ex:
            raise ex

    async def upload_file(self, sinister_id: UUID, file: UploadFile):
        try:
            content_file = await file.read()
            file_name = file.filename
            self.sinister_service.upload(content_file, file_name, sinister_id)
        except BaseHTTPException as ex:
            raise ex

    def download_file(self, sinister_id: UUID, file_name: str):
        try:
            file_path = self.sinister_service.get_download_path(
                sinister_id, file_name)
            return FileResponse(file_path)
        except BaseHTTPException as ex:
            raise ex

    def delete_file(self, sinister_id: UUID, file_name: str):
        try:
            self.sinister_service.delete_file(sinister_id, file_name)
        except BaseHTTPException as ex:
            raise ex
