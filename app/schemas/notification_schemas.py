from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .vehicle_schemas import VehicleResponse


class NotificationSchema(BaseModel):
    title: str
    message: str
    type: str
    is_read: bool
    vehicle_id: UUID

    class Config:
        orm_mode = True


class NotificationRequest(NotificationSchema):
    pass


class NotificationFilterRequest(BaseModel):
    title: str | None = None
    message: str | None = None
    type: str | None = None
    is_read: bool | None = None
    vehicle_id: UUID | None = None


class NotificationResponse(NotificationSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
    vehicle: VehicleResponse | None = None
