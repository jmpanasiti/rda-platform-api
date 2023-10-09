from datetime import date
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .branch_schemas import BranchResponse


class VehicleSchema(BaseModel):
    registration_plate: str
    brand: str
    model: str
    year: int
    fire_extinguisher_expiration_date: date
    vtv_expiration_date: date
    documents_expiration_date: date
    next_service_date: date
    policy_number: str
    # scoring_3s: int
    engraved_parts: bool
    fee: float
    chassis: str
    branch_id: UUID | None

    class Config:
        orm_mode = True


class VehicleRequest(VehicleSchema):
    fee: float | None = None
    branch_id: UUID


class VehicleResponse(VehicleSchema):
    id: UUID
    policy_file: str
    id_card_file: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    branch: BranchResponse | None = None
