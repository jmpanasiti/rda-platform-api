from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

from ..core.enums.sinister_enum import SinisterPlaceEnum
from ..core.enums.sinister_enum import SinisterStatusEnum
from ..core.enums.sinister_enum import SinisterTypeEnum
from .user_schemas import UserResponse
from .vehicle_schemas import VehicleResponse


class SinisterSchema(BaseModel):
    details_damage: str
    details_event: str
    type: SinisterTypeEnum
    status: SinisterStatusEnum
    place: SinisterPlaceEnum
    vehicle_id: UUID
    user_id: UUID

    class Config:
        orm_mode = True


class SinisterRequest(SinisterSchema):
    pass


class SinisterResponse(SinisterSchema):
    id: UUID
    files_urls: List[str]
    vehicle: VehicleResponse | None = None
    user: UserResponse | None = None
    approver_user_id: UUID | None = None
    created_at: datetime
    updated_at: datetime
