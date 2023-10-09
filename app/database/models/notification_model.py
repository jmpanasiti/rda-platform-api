from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import UUID
from sqlalchemy.orm import relationship

from . import BaseModel


class NotificationModel(BaseModel):
    __tablename__ = 'notifications'
    title = Column(String, nullable=False)
    message = Column(String, nullable=False, default="")
    # SUGERENCIAS O NOTIFICACIONES
    type = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey(
        'vehicles.id'), nullable=False)

    vehicle = relationship('VehicleModel', back_populates='notifications', foreign_keys=[
        vehicle_id], lazy='joined')
