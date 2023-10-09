from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator

from ..core.enums.role_enum import RoleEnum
from .branch_schemas import BranchResponse
from .driver_license_schemas import DriverLicenseResponse
from .vehicle_schemas import VehicleResponse


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    role: RoleEnum
    first_name: str
    last_name: str
    phone: str = ''
    job: str = ''
    branch_id: UUID | None = None
    vehicle_id: UUID | None = None

    class Config:
        orm_mode = True

    @validator('username')
    def username_is_valid(cls, value: str):
        if not value:
            raise ValueError('Username cannot be empty')
        if value[0].isdigit():
            raise ValueError('Username must not start with a number')
        if not all(c.isalnum() or c == '_' for c in value):
            raise ValueError(
                'Username must contain only letters, numbers and underscores')
        if not 5 <= len(value) <= 15:
            raise ValueError(
                'Username length must be between 5 and 15 characters')
        return value


class UserRequest(UserSchema):
    password: str | None = None  # Can be None just in update

    @validator('password')
    def password_is_valid(cls, value):
        if not value:
            raise ValueError('Password cannot be empty')
        if not 8 <= len(value) <= 32:
            raise ValueError(
                'Password length must be between 8 and 32 characters')
        return value


class UserUpdateRequest(UserRequest):
    username: str | None = None
    email: EmailStr | None = None
    role: RoleEnum | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    job: str | None = None


class UserResponse(UserSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool
    branch: BranchResponse | None = None
    vehicle: VehicleResponse | None = None
    driver_license: List[DriverLicenseResponse]


class FirstSuperAdmin(BaseModel):
    username: str
    email: EmailStr
    password: str
