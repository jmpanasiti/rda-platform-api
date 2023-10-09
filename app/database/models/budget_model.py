from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

from . import BaseModel


class BudgetModel(BaseModel):
    __tablename__ = 'budgets'

    detail = Column(String, nullable=False)
    allocation_file = Column(String, default='')
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    status = Column(String, nullable=False)
    approval_date = Column(Date, nullable=True)
    approved = Column(Boolean, default=False, nullable=False)
    effective_until_date = Column(Date, default='', nullable=False)
    # request_id = Column(UUID(as_uuid=True), ForeignKey('requests.id'))
    work_order_id = Column(UUID(as_uuid=True), ForeignKey('work_orders.id'))
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey('vehicles.id'))
    organization_id = Column(
        UUID(as_uuid=True), ForeignKey('organizations.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    # proovedor
