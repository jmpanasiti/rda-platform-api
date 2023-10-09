from typing import List
from uuid import UUID

from pydantic import BaseModel
from pydantic import EmailStr

from .user_schemas import UserResponse


class MyReportSchema (BaseModel):
    pass


class MyReportVehicleRes(BaseModel):
    id: UUID
    registration_plate: str
    is_active: bool = True
    brand: str
    model: str
    year: int
    fee: int
    users: List[UserResponse] = []


class MyReportUserRes(BaseModel):
    user_id: UUID
    is_active: bool = True
    email: EmailStr
    first_name: str
    last_name: str
