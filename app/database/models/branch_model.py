from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from . import BaseModel


class BranchModel(BaseModel):
    __tablename__ = 'branches'

    name = Column(String, nullable=False)
    cost_center = Column(String, nullable=False)
    area = Column(String, nullable=False)
    purchase_order_sent_date = Column(Date, nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey(
        'organizations.id'), nullable=False)
    agent_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id'), nullable=True)

    # Relationships
    users = relationship('UserModel', back_populates='branch',
                         viewonly=True, foreign_keys='UserModel.branch_id')

    organization = relationship(
        'OrganizationModel', viewonly=True, back_populates='branches', foreign_keys=[organization_id])
    vehicles = relationship(
        'VehicleModel',
        viewonly=True,
    )
    agent = relationship('UserModel', foreign_keys=[agent_id])
