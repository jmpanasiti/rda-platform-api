from ..database.models import WorkOrderModel
from ..repository.work_order_repository import WorkOrderRepository as WorkOrderRepo
from ..schemas.work_order_schemas import WorkOrderRequest
from ..schemas.work_order_schemas import WorkOrderResponse
from .base_service import BaseService


class WorkOrderService(BaseService[WorkOrderModel, WorkOrderRequest, WorkOrderResponse, WorkOrderRepo]):

    def __init__(self):
        super().__init__(WorkOrderRepo)

    def _to_schema(self, model: WorkOrderModel | dict, *args) -> WorkOrderResponse:
        if type(model) is dict:
            return WorkOrderResponse(**model)

        return WorkOrderResponse(
            id=model.id,
            name=model.name,
            status=model.status,
            vehicle_id=model.vehicle_id,
            vehicle=model.vehicle,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
