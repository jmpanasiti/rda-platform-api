from datetime import date
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DriverLicenseSchema(BaseModel):
    file_name: str
    file_type: str

    class Config:
        orm_mode = True


class DriverLicenseRequest(DriverLicenseSchema):
    expiration_date: date
    content_file: bytes
    user_id: UUID


class DriverLicenseResponse(DriverLicenseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
