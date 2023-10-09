import logging
from typing import List
from uuid import UUID

from app.exceptions.base_http_exception import BaseHTTPException
from app.schemas.purchase_order_schemas import PurchaseOrderRequest
from app.schemas.purchase_order_schemas import PurchaseOrderResponse
from app.service.purchase_order_service import PurchaseOrderService
# from fastapi import UploadFile # TODO: implements upload for the po file

logger = logging.getLogger(__name__)


class PurchaseOrderController():
    def __init__(self) -> None:
        self.__purchase_order_service = None

    @property
    def purchase_order_service(self) -> PurchaseOrderService:
        if self.__purchase_order_service is None:
            self.__purchase_order_service = PurchaseOrderService()
        return self.__purchase_order_service

    def create(self, po_request: PurchaseOrderRequest) -> PurchaseOrderResponse:
        try:
            return self.purchase_order_service.create(po_request)
        except BaseHTTPException as ex:
            raise ex

    def get_list(self, limit: int, offset: int) -> List[PurchaseOrderResponse]:
        try:
            return self.purchase_order_service.get_all(limit, offset)
        except BaseHTTPException as ex:
            raise ex

    def get_by_id(self, po_id: UUID) -> PurchaseOrderResponse:
        try:
            return self.purchase_order_service.get_by_id(po_id)
        except BaseHTTPException as ex:
            raise ex

    def update(self,  po_id: UUID, po_data: PurchaseOrderRequest) -> PurchaseOrderResponse:
        try:
            return self.purchase_order_service.update(po_id, po_data)
        except BaseHTTPException as ex:
            raise ex

    def delete(self, po_id: UUID) -> None:
        try:
            return self.purchase_order_service.delete(po_id)
        except BaseHTTPException as ex:
            raise ex
