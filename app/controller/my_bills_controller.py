import logging
from typing import List
from uuid import UUID

from app.schemas.my_bills_schemas import MyBillsPOReq
from app.schemas.my_bills_schemas import MyBillsPORes
from app.schemas.my_bills_schemas import MyBillsPOUpdateReq
from app.service.my_bills_service import MyBillsService

logger = logging.getLogger(__name__)


class MyBillsController():
    def __init__(self) -> None:
        self.__service = None

    @property
    def service(self) -> MyBillsService:
        if self.__service is None:
            self.__service = MyBillsService()
        return self.__service

    def get_po_paginated(self, limit: int, offset: int, branch_id: UUID) -> List[MyBillsPORes]:
        return self.service.get_purchase_order_list(branch_id, limit, offset)

    def get_po_by_id(self, branch_id: UUID, purchase_order_id: UUID) -> MyBillsPORes:
        return self.service.get_purchase_order_by_id(branch_id, purchase_order_id)

    def add_new_po(self, branch_id: UUID, purchase_order: MyBillsPOReq) -> MyBillsPORes:
        return self.service.create_new_purchase_order(branch_id, purchase_order)

    def update_po(self, branch_id: UUID, purchase_order_id: UUID, purchase_order: MyBillsPOUpdateReq) -> MyBillsPORes:
        return self.service.update_purchase_order(branch_id, purchase_order_id, purchase_order)

    def delete_po(self, branch_id: UUID, purchase_order_id: UUID) -> None:
        return self.service.delete_purchase_order(branch_id, purchase_order_id)
