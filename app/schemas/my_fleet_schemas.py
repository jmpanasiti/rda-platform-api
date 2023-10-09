from datetime import date
from datetime import datetime
from datetime import timedelta
from typing import List
from uuid import UUID

from pydantic import BaseModel
from pydantic import EmailStr

from .branch_schemas import BranchResponse
from .driver_license_schemas import DriverLicenseResponse
from .user_schemas import UserResponse
from app.core.enums.role_enum import RoleEnum


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
    users: List[UserResponse] = []
    branch_id: UUID | None
    chassis: str
    is_active: bool

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
