from ..database.models import PurchaseOrderModel
from ..repository.purchase_order_repository import PurchaseOrderRepository as PurchaseOrderRepo
from ..schemas.purchase_order_schemas import PurchaseOrderRequest
from ..schemas.purchase_order_schemas import PurchaseOrderResponse
from .base_service import BaseService


class PurchaseOrderService(BaseService[PurchaseOrderModel, PurchaseOrderRequest, PurchaseOrderResponse, PurchaseOrderRepo]):

    def __init__(self):
        super().__init__(PurchaseOrderRepo)

    def _to_schema(self, model: PurchaseOrderModel | dict, *args) -> PurchaseOrderResponse:
        if type(model) is dict:
            return PurchaseOrderResponse(**model)

        return PurchaseOrderResponse(
            id=model.id,
            number=model.number,
            amount=model.amount,
            expires=model.expires,
            due_date=model.due_date,
            file_path=model.file_path,
            branch_id=model.branch_id,
        )
