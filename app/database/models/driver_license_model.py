from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship

from . import BaseModel


class DriverLicenseModel(BaseModel):
    __tablename__ = 'driver_licenses'

    expiration_date = Column(Date, nullable=False)
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id'), nullable=False)
    user = relationship('UserModel', uselist=False,
                        backref=backref('license', uselist=False))
