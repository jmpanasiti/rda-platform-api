from datetime import date
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.core.enums.budget_status_enum import BudgetStatusEnum


class BudgetRequest(BaseModel):
    approved: bool = False
    amount: float
    detail: str
    effective_until_date: date | None = None
    vehicle_id: UUID
    organization_id: UUID
    user_id: UUID
    status: BudgetStatusEnum = BudgetStatusEnum.PENDING
    work_order_id: UUID | None = None


class BudgetResponse(BaseModel):
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    id: UUID
    amount: float
    detail: str
    approval_date: date | None = None
    status: BudgetStatusEnum
    work_order_id: UUID | None = None
    vehicle_id: UUID
