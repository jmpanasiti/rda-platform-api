from datetime import date
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ..core.enums.vehicle_enum import CoverageTypeEnum
from ..core.enums.vehicle_enum import FuelTypeEnum
from ..core.enums.vehicle_enum import OwnershipEnum
from ..core.enums.vehicle_enum import PurchaseTypeEnum
from ..core.enums.vehicle_enum import VehicleStatusEnum
from ..core.enums.vehicle_enum import VehicleTypeEnum
from .branch_schemas import BranchResponse


class VehicleSchema(BaseModel):
    registration_plate: str
    brand: str
    model: str
    year: int
    version: str
    status: VehicleStatusEnum = ''
    type: VehicleTypeEnum
    color: str
    fuel_type: FuelTypeEnum
    fire_extinguisher_expiration_date: date
    vtv_expiration_date: date
    documents_expiration_date: date
    next_service_date: date
    engraved_parts_date: date
    purchase_date: date
    ensurance_expiration_date: date
    ruta_expiration_date: date
    auth_documents_expiration_date: date
    policy_number: str
    policy_url: str
    # scoring_3s: int
    engraved_parts: bool = False
    fee: float
    chassis: str
    engine: str
    tire_measure: str
    ensurance_name: str
    broker_name: str
    invoice_number: str
    vehicle_value: float
    purchase_value: float
    purchase_type: PurchaseTypeEnum
    coverage_type: CoverageTypeEnum
    ownership: OwnershipEnum
    franchise_deductible: int
    ensurance_company: str
    assistance: bool = False
    hooked: bool = False
    leasing: bool = False
    telemetry: bool = False
    armor: bool = False
    census: str

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
    auth_id_card_file: str
    title_file: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    branch: BranchResponse | None = None

    version: str | None = None
    status: VehicleStatusEnum | None = None
    type: VehicleTypeEnum | None = None
    color: str | None = None
    fuel_type: FuelTypeEnum | None = None
    engraved_parts_date: date | None = None
    purchase_date: date | None = None
    ensurance_expiration_date: date | None = None
    ruta_expiration_date: date | None = None
    auth_documents_expiration_date: date | None = None
    policy_url: str | None = None
    engine: str | None = None
    tire_measure: str | None = None
    ensurance_name: str | None = None
    broker_name: str | None = None
    invoice_number: str | None = None
    vehicle_value: float | None = None
    purchase_value: float | None = None
    purchase_type: PurchaseTypeEnum | None = None
    coverage_type: CoverageTypeEnum | None = None
    ownership: OwnershipEnum | None = None
    franchise_deductible: int | None = None
    ensurance_company: str | None = None
    assistance: bool | None = None
    hooked: bool | None = None
    leasing: bool | None = None
    telemetry: bool | None = None
    armor: bool | None = None
    census: str | None = None
    auth_id_card_file: str | None = None
    title_file: str | None = None
