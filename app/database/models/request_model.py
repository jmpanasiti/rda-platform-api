from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UUID
from sqlalchemy.orm import relationship

from . import BaseModel
from ...core.enums.request_enum import RequestStatusEnum as StatusEnum
from ...core.enums.request_enum import RequestTireReasonEnum as TireEnum
from ...core.enums.request_enum import RequestTypeEnum as TypeEnum
from ...core.enums.request_enum import RequestVerTypeEnum as VerTypeEnum


class RequestModel(BaseModel):
    __tablename__ = 'requests'

    type = Column(Enum(TypeEnum), nullable=False)
    status = Column(Enum(StatusEnum), nullable=False,
                    default=StatusEnum.OPEN)
    details = Column(String, default="")
    odometer = Column(Integer, nullable=False)
    appointment_date = Column(DateTime, default="")
    alternative_date = Column(DateTime, default="")
    emergency = Column(Boolean, default=False)
    tire_quantity = Column(Integer)
    tire_brand = Column(String, default="")
    tire_alternative_brand = Column(String, default="")
    tire_measure = Column(String, default="")
    tire_reason = Column(Enum(TireEnum), nullable=True,
                         default=TireEnum.WEARING)
    tire_image = Column(String, default="")
    zone = Column(String, default="")
    user_validation = Column(Boolean, default=False)
    verification_type = Column(Enum(VerTypeEnum), nullable=True,
                               default=VerTypeEnum.VTV)
    approver_user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id'), nullable=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id'), nullable=False)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey(
        'vehicles.id'), nullable=False)

    user = relationship('UserModel', back_populates='requests', foreign_keys=[
        user_id], lazy='joined')

    vehicle = relationship('VehicleModel', back_populates='requests', foreign_keys=[
        vehicle_id], lazy='joined')

    approver_user = relationship('UserModel', foreign_keys=[
        approver_user_id], lazy='joined')
