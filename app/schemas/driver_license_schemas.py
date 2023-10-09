from datetime import date
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DriverLicenseSchema(BaseModel):
    file_name: str
    file_type: str
    expiration_date: date

    class Config:
        orm_mode = True


class DriverLicenseRequest(DriverLicenseSchema):
    content_file: bytes
    user_id: UUID


class DriverLicenseResponse(DriverLicenseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
