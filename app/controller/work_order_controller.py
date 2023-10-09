import logging
from typing import List
from uuid import UUID

from app.exceptions import server_exceptions as se
from app.exceptions.base_http_exception import BaseHTTPException
from app.schemas.work_order_schemas import WorkOrderRequest
from app.schemas.work_order_schemas import WorkOrderResponse
from app.service.work_order_service import WorkOrderService

logger = logging.getLogger(__name__)


class WorkOrderController():
    def __init__(self) -> None:
        self.__work_order_service = None

    @property
    def work_order_service(self) -> WorkOrderService:
        if self.__work_order_service is None:
            self.__work_order_service = WorkOrderService()
        return self.__work_order_service

    def create(self, work_order: WorkOrderRequest) -> WorkOrderResponse:
        try:
            new_work_order = self.work_order_service.create(work_order)
            return new_work_order

        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.critical("Not handled error")
            logger.error('; '.join(ex.args))
            raise se.InternalServerError(
                'Something went wrong, contact the admin')

    def get_list_paginated(self, limit: int, offset: int) -> List[WorkOrderResponse]:
        try:
            work_order_list = self.work_order_service.get_all(limit, offset)

            return work_order_list
        except Exception as ex:
            logger.critical(f'Unhandled error: {"; ".join(ex.args)}')
            raise se.InternalServerError(
                'Something went wrong on listing work orders. Please contact the sysadmin')

    def get_by_id(self, work_order_id: UUID) -> WorkOrderResponse:
        try:
            return self.work_order_service.get_by_id(work_order_id)
        except BaseHTTPException as ex:
            raise ex

    def update(self, work_order_id: UUID, work_order_data: WorkOrderRequest) -> WorkOrderResponse:
        try:
            return self.work_order_service.update(work_order_id, work_order_data)
        except BaseHTTPException as ex:
            raise ex

    def delete(self, work_order_id: UUID) -> None:
        try:
            self.work_order_service.delete(work_order_id)
        except BaseHTTPException as ex:
            raise ex
