from datetime import date
from uuid import UUID

from pydantic import BaseModel


class MyBillsPORes(BaseModel):
    id: UUID
    number: int
    amount: float
    expires: bool
    due_date: date
    file_path: str


class MyBillsPOReq(BaseModel):
    number: int
    amount: float
    expires: bool
    due_date: date


class MyBillsPOUpdateReq(BaseModel):
    number: int | None = None
    amount: float | None = None
    expires: bool | None = None
    due_date: date | None = None
