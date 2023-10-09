from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

from ..core.enums.request_enum import RequestStatusEnum
from ..core.enums.request_enum import RequestTireReasonEnum
from ..core.enums.request_enum import RequestTypeEnum
from ..core.enums.request_enum import RequestVerTypeEnum
from ..core.enums.sinister_enum import SinisterPlaceEnum
from ..core.enums.sinister_enum import SinisterStatusEnum
from ..core.enums.sinister_enum import SinisterTypeEnum
from .user_schemas import UserResponse
from .vehicle_schemas import VehicleResponse


class OperationsRequestReq(BaseModel):
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


class OperationsRequestRes(BaseModel):
    id: UUID
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
    approver_user_id: UUID | None = None
    user: UserResponse
    vehicle: VehicleResponse

    class Config:
        orm_mode = True


class OperationsRequestUpdateReq(OperationsRequestReq):
    type: RequestTypeEnum | None = None
    status: RequestStatusEnum | None = None
    details: str | None = None
    odometer: int | None = None
    appointment_date: datetime | None = None
    alternative_date: datetime | None = None
    emergency: bool | None = None
    tire_quantity: int | None = None
    tire_brand: str | None = None
    tire_alternative_brand: str | None = None
    tire_measure: str | None = None
    tire_reason: RequestTireReasonEnum | None = None
    verification_type: RequestVerTypeEnum | None = None
    user_validation: bool | None = None


class OperationsSinisterReq(BaseModel):
    details_damage: str
    details_event: str
    type: SinisterTypeEnum
    status: SinisterStatusEnum
    place: SinisterPlaceEnum
    vehicle_id: UUID
    user_id: UUID


class OperationsSinisterRes(BaseModel):
    id: UUID
    files_urls: List[str]
    details_damage: str
    details_event: str
    type: SinisterTypeEnum
    status: SinisterStatusEnum
    place: SinisterPlaceEnum
    vehicle: VehicleResponse | None = None
    user: UserResponse | None = None
    approver_user_id: UUID | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class OperationsSinisterUpdateReq(OperationsSinisterReq):
    details_damage: str | None = None
    details_event: str | None = None
    type: SinisterTypeEnum | None = None
    status: SinisterStatusEnum | None = None
    place: SinisterPlaceEnum | None = None
