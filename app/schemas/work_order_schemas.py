from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ..core.enums.wo_status_enum import StatusEnum
from .vehicle_schemas import VehicleResponse


class WorkOrderSchema(BaseModel):
    name: str
    status: StatusEnum
    vehicle_id: UUID

    class Config:
        orm_mode = True


class WorkOrderRequest(WorkOrderSchema):
    pass


class WorkOrderResponse(WorkOrderSchema):
    id: UUID
    vehicle: VehicleResponse | None = None
    created_at: datetime
    updated_at: datetime
