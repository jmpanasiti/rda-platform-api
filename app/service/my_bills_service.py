import logging
from typing import List
from uuid import UUID

from app.repository.purchase_order_repository import PurchaseOrderRepository
from app.schemas.my_bills_schemas import MyBillsPOReq
from app.schemas.my_bills_schemas import MyBillsPORes
from app.schemas.my_bills_schemas import MyBillsPOUpdateReq

logger = logging.getLogger(__name__)


class MyBillsService():
    def __init__(self) -> None:
        self.__purchase_order_repo = None

    @property
    def purchase_order_repo(self) -> PurchaseOrderRepository:
        if self.__purchase_order_repo is None:
            self.__purchase_order_repo = PurchaseOrderRepository()
        return self.__purchase_order_repo

    def get_purchase_order_list(self, branch_id: UUID, limit: int, offset: int) -> List[MyBillsPORes]:
        try:
            purchase_orders = self.purchase_order_repo.get_all(
                limit,
                offset,
                search_filter={'branch_id': branch_id},
            )
            return [MyBillsPORes.from_orm(po) for po in purchase_orders]

        except Exception as ex:
            logger.critical(ex.args)

    def get_purchase_order_by_id(self, branch_id: UUID, po_id: UUID) -> MyBillsPORes:
        try:
            search_filter = {'branch_id': branch_id}
            purchase_order = self.purchase_order_repo.get_by_id(
                po_id, search_filter)
            return MyBillsPORes.from_orm(purchase_order)
        except Exception as ex:
            logger.critical(ex.args)

    def create_new_purchase_order(self, branch_id: UUID, purchase_order_req: MyBillsPOReq) -> MyBillsPORes:
        try:
            new_purchase_order = self.purchase_order_repo.create({
                **purchase_order_req.dict(),
                'branch_id': branch_id,
            })

            return MyBillsPORes.from_orm(new_purchase_order)
        except Exception as ex:
            logger.critical(ex.args)

    def update_purchase_order(self, branch_id: UUID, po_id: UUID,  purchase_order: MyBillsPOUpdateReq) -> MyBillsPORes:
        try:
            search_filter = {'branch_id': branch_id}

            # First checks if the PO belongs to the branch
            self.purchase_order_repo.get_by_id(po_id, search_filter)

            purchase_order = self.purchase_order_repo.update({
                **purchase_order.dict(),
                'branch_id': branch_id,
            })

            return MyBillsPORes.from_orm(purchase_order)
        except Exception as ex:
            logger.critical(ex.args)

    def delete_purchase_order(self, branch_id: UUID, po_id: UUID) -> None:
        try:
            search_filter = {'branch_id': branch_id}

            # First checks if the PO belongs to the branch
            self.purchase_order_repo.get_by_id(po_id, search_filter)
            self.purchase_order_repo.delete(po_id)
            return
        except Exception as ex:
            logger.critical(ex.args)
