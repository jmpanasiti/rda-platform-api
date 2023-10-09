from datetime import date
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .organization_schemas import OrganizationResponse


class BranchSchema(BaseModel):
    name: str
    cost_center: str
    area: str
    purchase_order_sent_date: date | None
    organization_id: UUID
    agent_id: UUID | None

    class Config:
        orm_mode = True


class BranchRequest(BranchSchema):
    pass


class BranchResponse(BranchSchema):
    id: UUID
    organization: OrganizationResponse | None = None
    created_at: datetime
    updated_at: datetime
