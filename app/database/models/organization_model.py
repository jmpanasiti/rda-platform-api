from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from . import BaseModel
# from sqlalchemy.orm import backref


class OrganizationModel(BaseModel):
    __tablename__ = 'organizations'

    name = Column(String, nullable=False)
    super_manager_id = Column(
        UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    contact_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id'), nullable=False)
    business_name = Column(String, nullable=False)

    # relations
    # super_manager = relationship('UserModel', uselist=False, backref=backref('organization_managed', uselist=False))
    # contact = relationship('UserModel', uselist=False, backref=backref('organization_contact', uselist=False))
    branches = relationship('BranchModel', back_populates='organization',
                            foreign_keys='BranchModel.organization_id')
