import logging
from typing import List
from uuid import UUID

from app.exceptions import server_exceptions as se
from app.exceptions.base_http_exception import BaseHTTPException
from app.schemas.request_schemas import ServiceRequestReq
from app.schemas.request_schemas import ServiceRequestRes
from app.service.request_service import RequestService

logger = logging.getLogger(__name__)


class RequestController():
    def __init__(self) -> None:
        self.__request_service = None

    @property
    def request_service(self) -> RequestService:
        if self.__request_service is None:
            self.__request_service = RequestService()
        return self.__request_service

    def create(self, request: ServiceRequestReq) -> ServiceRequestRes:
        try:
            new_request = self.request_service.create(request)
            return new_request

        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.critical("Not handled error")
            logger.error('; '.join(ex.args))
            raise se.InternalServerError(
                'Something went wrong, contact the admin')

    def get_list_paginated(self, limit: int, offset: int) -> List[ServiceRequestRes]:
        try:
            request_list = self.request_service.get_all(limit, offset)

            return request_list
        except Exception as ex:
            logger.critical(f'Unhandled error: {"; ".join(ex.args)}')
            raise se.InternalServerError(
                'Something went wrong on listing requests. Please contact the sysadmin')

    def get_by_id(self, request_id: UUID) -> ServiceRequestRes:
        try:
            return self.request_service.get_by_id(request_id)
        except BaseHTTPException as ex:
            raise ex

    def update(self, request_id: UUID, request_data: ServiceRequestReq) -> ServiceRequestRes:
        try:
            return self.request_service.update(request_id, request_data)
        except BaseHTTPException as ex:
            raise ex

    def delete(self, request_id: UUID) -> None:
        try:
            self.request_service.delete(request_id)
        except BaseHTTPException as ex:
            raise ex
