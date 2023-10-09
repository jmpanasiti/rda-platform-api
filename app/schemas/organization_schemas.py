from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class OrganizationSchema(BaseModel):
    name: str
    business_name: str
    contact_id: UUID | None = None
    super_manager_id: UUID | None = None

    class Config:
        orm_mode = True


class OrganizationRequest(OrganizationSchema):
    pass


class OrganizationResponse(OrganizationSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
