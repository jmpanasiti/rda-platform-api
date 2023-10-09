from datetime import date
from uuid import UUID

from pydantic import BaseModel
from pydantic import validator

from .branch_schemas import BranchResponse


class PurchaseOrderSchema(BaseModel):
    number: int
    amount: float
    expires: bool = False
    due_date: date | None = None
    file_path: str | None = None
    branch_id: UUID

    @validator('due_date')
    def validate_due_date(cls, due_date: date, values: dict) -> date:
        if values.get('expires') and due_date is not None and due_date < date.today():
            raise ValueError(
                "The expiration date cannot be earlier than the current day.")
        return due_date

    class Config:
        orm_mode = True


class PurchaseOrderRequest(PurchaseOrderSchema):
    pass


class PurchaseOrderResponse(PurchaseOrderSchema):
    id: UUID
    branch: BranchResponse | None = None
