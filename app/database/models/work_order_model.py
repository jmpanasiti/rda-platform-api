from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from . import BaseModel
from ...core.enums.wo_status_enum import StatusEnum


class WorkOrderModel(BaseModel):
    __tablename__ = 'work_orders'

    name = Column(String, nullable=False)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.OPEN)

    vehicle_id = Column(UUID(as_uuid=True), ForeignKey(
        'vehicles.id'), nullable=False)

    vehicle = relationship('VehicleModel', back_populates='work_orders', foreign_keys=[
        vehicle_id], lazy='joined')
