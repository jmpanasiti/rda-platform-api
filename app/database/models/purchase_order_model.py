from datetime import date

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

from . import BaseModel
# from sqlalchemy.orm import relationship  # TODO: Implements relationship with branch


class PurchaseOrderModel(BaseModel):
    __tablename__ = 'purchase_orders'

    number = Column(Integer(), nullable=False)
    amount = Column(Float(), nullable=False)
    expires = Column(Boolean(), default=False, nullable=False)
    due_date = Column(Date(), default=date.today(), nullable=False)
    file_path = Column(String(255), default='', nullable=False)

    branch_id = Column(UUID(as_uuid=True), ForeignKey(
        'branches.id'), nullable=False)
