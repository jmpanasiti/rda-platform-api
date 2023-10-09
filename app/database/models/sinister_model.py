from sqlalchemy import ARRAY
from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import UUID
from sqlalchemy.orm import relationship

from . import BaseModel
from ...core.enums.sinister_enum import SinisterPlaceEnum
from ...core.enums.sinister_enum import SinisterStatusEnum
from ...core.enums.sinister_enum import SinisterTypeEnum


class SinisterModel(BaseModel):
    __tablename__ = 'sinisters'

    status = Column(Enum(SinisterStatusEnum), nullable=False,
                    default=SinisterStatusEnum.OPEN)
    files_urls = Column(ARRAY(String), default=[])
    details_damage = Column(String, default="")
    details_event = Column(String, default="")
    type = Column(Enum(SinisterTypeEnum), nullable=False)
    place = Column(Enum(SinisterPlaceEnum), nullable=False)
    zone = Column(String, default="")
    approver_user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id'), nullable=True)

    vehicle_id = Column(UUID(as_uuid=True), ForeignKey(
        'vehicles.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id'), nullable=False)

    vehicle = relationship('VehicleModel', back_populates='sinisters', foreign_keys=[
        vehicle_id], lazy='joined')

    user = relationship('UserModel', back_populates='sinisters', foreign_keys=[
        user_id], lazy='joined')

    approver_user = relationship('UserModel', foreign_keys=[
        approver_user_id], lazy='joined')
