from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UUID
from sqlalchemy.orm import relationship

from . import BaseModel


class VehicleModel(BaseModel):
    __tablename__ = 'vehicles'
    registration_plate = Column(
        String(25), unique=True, index=True, default='')
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    fire_extinguisher_expiration_date = Column(Date, default='')
    vtv_expiration_date = Column(Date, default='')
    documents_expiration_date = Column(Date, default='')
    next_service_date = Column(Date, default='')
    policy_number = Column(String, default='')
    # scoring_3s = Column(Integer, default='')
    engraved_parts = Column(Boolean, default=False)
    policy_file = Column(String, default='')
    id_card_file = Column(String, default='')
    is_active = Column(Boolean, default=True)
    fee = Column(Float(), nullable=False, default=0.0)
    chassis = Column(String(30), nullable=False, default='')

    branch_id = Column(UUID(as_uuid=True), ForeignKey('branches.id'))

    work_orders = relationship('WorkOrderModel', back_populates='vehicle',
                               foreign_keys='WorkOrderModel.vehicle_id')

    users = relationship('UserModel', back_populates='vehicle',
                         foreign_keys='UserModel.vehicle_id')

    requests = relationship('RequestModel', back_populates='vehicle',
                            foreign_keys='RequestModel.vehicle_id')

    sinisters = relationship('SinisterModel', back_populates='vehicle',
                             foreign_keys='SinisterModel.vehicle_id')

    notifications = relationship('NotificationModel', back_populates='vehicle',
                                 foreign_keys='NotificationModel.vehicle_id')
