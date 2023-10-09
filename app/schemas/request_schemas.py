from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ..core.enums.request_enum import RequestStatusEnum
from ..core.enums.request_enum import RequestTireReasonEnum
from ..core.enums.request_enum import RequestTypeEnum
from ..core.enums.request_enum import RequestVerTypeEnum
from .user_schemas import UserResponse
from .vehicle_schemas import VehicleResponse


class ServiceRequestSchema(BaseModel):
    type: RequestTypeEnum
    status: RequestStatusEnum
    details: str
    odometer: int
    appointment_date: datetime
    alternative_date: datetime
    emergency: bool
    tire_quantity: int
    tire_brand: str
    tire_alternative_brand: str
    tire_measure: str
    tire_image: str
    tire_reason: RequestTireReasonEnum
    verification_type: RequestVerTypeEnum
    user_validation: bool
    zone: str

    vehicle_id: UUID
    user_id: UUID

    class Config:
        orm_mode = True


class ServiceRequestReq(ServiceRequestSchema):
    pass


class ServiceRequestRes(ServiceRequestSchema):
    id: UUID
    vehicle: VehicleResponse | None = None
    user: UserResponse | None = None
    approver_user_id: UUID | None = None
    created_at: datetime
    updated_at: datetime
