import logging
from typing import List
from uuid import UUID

from fastapi import UploadFile
from fastapi.responses import FileResponse

from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.exceptions.base_http_exception import BaseHTTPException
from app.schemas.vehicle_schemas import VehicleRequest
from app.schemas.vehicle_schemas import VehicleResponse
from app.service.vehicle_service import VehicleService

logger = logging.getLogger(__name__)


class VehicleController():
    def __init__(self) -> None:
        self.__vehicle_service = None

    @property
    def vehicle_service(self) -> VehicleService:
        if self.__vehicle_service is None:
            self.__vehicle_service = VehicleService()
        return self.__vehicle_service

    def create(self, vehicle: VehicleRequest) -> VehicleResponse:
        try:
            new_vehicle = self.vehicle_service.create(vehicle)
            return new_vehicle
        except ce.BadRequest as ex:
            raise ex
        except Exception as ex:
            logger.critical("Not handled error")
            logger.error('; '.join(ex.args))
            raise se.InternalServerError(
                'Something went wrong, contact the admin')

    def get_list_paginated(self, limit: int, offset: int) -> List[VehicleResponse]:
        try:
            response = self.vehicle_service.get_all(limit, offset)
            return response
        except Exception as ex:
            logger.critical(f'Unhandled error: {"; ".join(ex.args)}')
            raise se.InternalServerError(
                'Something went wrong on listing orgs. Please contact the sysadmin')

    def get_by_id(self, vehicle_id: UUID):
        try:
            response = self.vehicle_service.get_by_id(vehicle_id)
            return response
        except ce.NotFound as ex:
            raise ex

    def update(self, vehicle_id: UUID, vehicle_data: VehicleRequest) -> VehicleResponse:
        try:
            response = self.vehicle_service.update(vehicle_id, vehicle_data)
            return response
        except ce.NotFound as ex:
            raise ex

    def delete(self, vehicle_id: UUID):
        try:
            self.vehicle_service.delete(vehicle_id)
        except ce.NotFound as ex:
            raise ex

    def activate(self, vehicle_id: UUID):
        try:
            return self.vehicle_service.activate(vehicle_id)
        except BaseHTTPException as ex:
            raise ex

    def deactivate(self, vehicle_id: UUID):
        try:
            return self.vehicle_service.deactivate(vehicle_id)
        except BaseHTTPException as ex:
            raise ex

    async def upload_policy(self, vehicle_id: UUID, file: UploadFile):
        try:
            content_file = await file.read()
            file_name = file.filename
            self.vehicle_service.upload_policy(
                content_file, file_name, vehicle_id)
        except BaseHTTPException as ex:
            raise ex

    async def upload_idcard(self, vehicle_id: UUID, file: UploadFile):
        try:
            content_file = await file.read()
            file_name = file.filename
            self.vehicle_service.upload_idcard(
                content_file, file_name, vehicle_id)
        except BaseHTTPException as ex:
            raise ex

    def download_policy(self, vehicle_id: UUID, file_name: str):
        try:
            file_path = self.vehicle_service.get_download_path_policy(
                vehicle_id, file_name)
            return FileResponse(file_path)
        except BaseHTTPException as ex:
            raise ex

    def download_idcard(self, vehicle_id: UUID, file_name: str):
        try:
            file_path = self.vehicle_service.get_download_path_idcard(
                vehicle_id, file_name)
            return FileResponse(file_path)
        except BaseHTTPException as ex:
            raise ex

    def delete_policy(self, vehicle_id: UUID, file_name: str):
        try:
            self.vehicle_service.delete_policy(vehicle_id, file_name)
        except BaseHTTPException as ex:
            raise ex

    def delete_idcard(self, vehicle_id: UUID, file_name: str):
        try:
            self.vehicle_service.delete_idcard(vehicle_id, file_name)
        except BaseHTTPException as ex:
            raise ex
