from datetime import date
from datetime import datetime
from datetime import timedelta
from typing import List
from uuid import UUID

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

from ..core.enums.vehicle_enum import CoverageTypeEnum
from ..core.enums.vehicle_enum import FuelTypeEnum
from ..core.enums.vehicle_enum import OwnershipEnum
from ..core.enums.vehicle_enum import PurchaseTypeEnum
from ..core.enums.vehicle_enum import VehicleStatusEnum
from ..core.enums.vehicle_enum import VehicleTypeEnum
from .branch_schemas import BranchResponse
from .driver_license_schemas import DriverLicenseResponse
from app.core.enums.role_enum import RoleEnum


class SimpleUser(BaseModel):
    username: str
    email: EmailStr
    role: RoleEnum
    first_name: str
    last_name: str
    phone: str = ''
    job: str = ''
    branch_id: UUID | None = None
    vehicle_id: UUID | None = None
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool
    driver_license: List[DriverLicenseResponse] | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {
            "username": Field(default=None),
            "email": Field(default=None),
            "role": Field(default=None),
            "first_name": Field(default=None),
            "last_name": Field(default=None),
        }


class MyFleetVehicleRes(BaseModel):
    id: UUID
    registration_plate: str
    brand: str
    model: str
    year: int
    fire_extinguisher_expiration_date: date
    vtv_expiration_date: date
    documents_expiration_date: date
    next_service_date: date
    policy_number: str
    engraved_parts: bool
    policy_file: str
    id_card_file: str
    users: List[SimpleUser] = []
    branch_id: UUID | None
    chassis: str
    is_active: bool
    version: str | None = ''
    status: VehicleStatusEnum | None = ''
    type: VehicleTypeEnum | None = ''
    color: str | None = ''
    fuel_type: FuelTypeEnum | None = ''
    documents_expiration_date: date | None = ''
    next_service_date: date | None = ''
    engraved_parts_date: date | None = ''
    purchase_date: date | None = ''
    ensurance_expiration_date: date | None = ''
    ruta_expiration_date: date | None = ''
    auth_documents_expiration_date: date | None = ''
    policy_number: str | None = ''
    policy_url: str | None = ''
    engraved_parts: bool | None = False
    fee: float | None = 0
    chassis: str | None = ''
    engine: str | None = ''
    tire_measure: str | None = ''
    ensurance_name: str | None = ''
    broker_name: str | None = ''
    invoice_number: str | None = ''
    vehicle_value: float | None = 0
    purchase_value: float | None = 0
    purchase_type: PurchaseTypeEnum | None = ''
    coverage_type: CoverageTypeEnum | None = ''
    ownership: OwnershipEnum | None = ''
    franchise_deductible: int | None = 0
    ensurance_company: str | None = ''
    assistance: bool | None = False
    hooked: bool | None = False
    leasing: bool | None = False
    telemetry: bool | None = False
    armor: bool | None = False
    census: str | None = ''

    branch_id: UUID | None = None

    class Config:
        orm_mode = True


class MyFleetVehicleReq(BaseModel):
    registration_plate: str
    brand: str
    model: str
    year: int
    fire_extinguisher_expiration_date: date
    vtv_expiration_date: date
    documents_expiration_date: date
    next_service_date: date
    policy_number: str
    engraved_parts: bool = False
    is_active: bool = True
    chassis: str

    version: str | None = ''
    status: VehicleStatusEnum | None = ''
    type: VehicleTypeEnum | None = ''
    color: str | None = ''
    fuel_type: FuelTypeEnum | None = ''
    documents_expiration_date: date | None = ''
    next_service_date: date | None = ''
    engraved_parts_date: date | None = ''
    purchase_date: date | None = ''
    ensurance_expiration_date: date | None = ''
    ruta_expiration_date: date | None = ''
    auth_documents_expiration_date: date | None = ''
    policy_number: str | None = ''
    policy_url: str | None = ''
    engraved_parts: bool | None = False
    fee: float | None = 0
    chassis: str | None = ''
    engine: str | None = ''
    tire_measure: str | None = ''
    ensurance_name: str | None = ''
    broker_name: str | None = ''
    invoice_number: str | None = ''
    vehicle_value: float | None = 0
    purchase_value: float | None = 0
    purchase_type: PurchaseTypeEnum | None = ''
    coverage_type: CoverageTypeEnum | None = ''
    ownership: OwnershipEnum | None = ''
    franchise_deductible: int | None = 0
    ensurance_company: str | None = ''
    assistance: bool | None = False
    hooked: bool | None = False
    leasing: bool | None = False
    telemetry: bool | None = False
    armor: bool | None = False
    census: str | None = ''

    branch_id: UUID | None = None

    class Config:
        orm_mode = True
        schema_extra = {
            'registration_plate': 'AA000AA',
            'brand': 'VW',
            'model': 'Vento',
            'year': 2020,
            'fire_extinguisher_expiration_date': datetime.now().date() + timedelta(days=365),
            'vtv_expiration_date': datetime.now().date() + timedelta(days=365),
            'documents_expiration_date': datetime.now().date() + timedelta(days=365),
            'next_service_date': datetime.now().date() + timedelta(days=365),
            'policy_number': 'TR001-002',
            'engraved_parts': True,
            'is_active': True,
            'chassis': '',
        }


class MyFleetVehicleUpdateReq(MyFleetVehicleReq):
    registration_plate: str | None = None
    brand: str | None = None
    model: str | None = None
    year: int | None = None
    fire_extinguisher_expiration_date: date | None = None
    vtv_expiration_date: date | None = None
    documents_expiration_date: date | None = None
    next_service_date: date | None = None
    policy_number: str | None = None
    engraved_parts: bool | None = None
    is_active: bool | None = None

    version: str | None = ''
    status: VehicleStatusEnum | None = ''
    type: VehicleTypeEnum | None = ''
    color: str | None = ''
    fuel_type: FuelTypeEnum | None = ''
    documents_expiration_date: date | None = ''
    next_service_date: date | None = ''
    engraved_parts_date: date | None = ''
    purchase_date: date | None = ''
    ensurance_expiration_date: date | None = ''
    ruta_expiration_date: date | None = ''
    auth_documents_expiration_date: date | None = ''
    policy_number: str | None = ''
    policy_url: str | None = ''
    engraved_parts: bool | None = False
    fee: float | None = 0
    chassis: str | None = ''
    engine: str | None = ''
    tire_measure: str | None = ''
    ensurance_name: str | None = ''
    broker_name: str | None = ''
    invoice_number: str | None = ''
    vehicle_value: float | None = 0
    purchase_value: float | None = 0
    purchase_type: PurchaseTypeEnum | None = ''
    coverage_type: CoverageTypeEnum | None = ''
    ownership: OwnershipEnum | None = ''
    franchise_deductible: int | None = 0
    ensurance_company: str | None = ''
    assistance: bool | None = False
    hooked: bool | None = False
    leasing: bool | None = False
    telemetry: bool | None = False
    armor: bool | None = False
    census: str | None = ''

    branch_id: UUID | None = None


class MyFleetUserRes(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    phone: str
    job: str
    is_active: bool
    vehicle_id: UUID | None
    role: RoleEnum
    branch: BranchResponse | None = None
    branch_id: UUID | None
    driver_license: List[DriverLicenseResponse]

    class Config:
        orm_mode = True


class MyFleetUserReq(BaseModel):
    username: str
    password: str
    email: EmailStr
    first_name: str
    last_name: str
    phone: str = ''
    job: str = ''
    is_active: bool = True
    vehicle_id: UUID | None = None
    role: RoleEnum = RoleEnum.driver
    branch_id: UUID | None

    class Config:
        orm_mode = True


class MyFleetUserUpdateReq(MyFleetUserReq):
    username: str | None = None
    password: str | None = None
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    job: str | None = None
    is_active: bool | None = None
    vehicle_id: UUID | None = None
    role: RoleEnum | None = None
    branch_id: UUID | None
