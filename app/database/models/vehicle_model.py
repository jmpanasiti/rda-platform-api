from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
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
    version = Column(String(30), default='')
    status = Column(String, nullable=False, default='')
    type = Column(String, default='')
    color = Column(String, default='')
    fuel_type = Column(String(20), nullable=True)
    fire_extinguisher_expiration_date = Column(Date, default='')
    vtv_expiration_date = Column(Date, default='')
    documents_expiration_date = Column(Date, default='')
    auth_documents_expiration_date = Column(Date, default='')
    ruta_expiration_date = Column(Date, default='')
    next_service_date = Column(Date, default='')
    ensurance_expiration_date = Column(Date, default='')
    policy_number = Column(String, default='')
    # scoring_3s = Column(Integer, default='')
    engraved_parts = Column(Boolean, default=False)
    engraved_parts_date = Column(Date, default='')
    policy_file = Column(String, default='')
    id_card_file = Column(String, default='')
    title_file = Column(String, default='')
    auth_id_card_file = Column(String, default='')
    census = Column(String(30), default='')
    is_active = Column(Boolean, default=True)
    armor = Column(Boolean, default=False)
    telemetry = Column(Boolean, default=False)
    leasing = Column(Boolean, default=False)
    hooked = Column(Boolean, default=False)
    assistance = Column(Boolean, default=False)
    ensurance_company = Column(String, default='')
    franchise_deductible = Column(Integer, nullable=True)
    policy_url = Column(String, default='')
    coverage_type = Column(String(30), default='')
    purchase_type = Column(String(30), default='')
    ownership = Column(String(30), default='')
    purchase_date = Column(Date, default='')
    purchase_value = Column(Numeric(precision=10, scale=2), default='')
    vehicle_value = Column(Numeric(precision=10, scale=2), default='')
    invoice_number = Column(String, default='')
    broker_name = Column(String, default='')
    ensurance_name = Column(String, default='')
    tire_measure = Column(String, default='')
    fee = Column(Float(), nullable=False, default=0.0)
    chassis = Column(String(30), nullable=False, default='')
    engine = Column(String(30), nullable=True, default='')

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
