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
    manager_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id'), nullable=True)
    contact_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id'), nullable=False)
    business_name = Column(String, nullable=False)
    document_number = Column(String(20), nullable=True)

    # relations
    # super_manager = relationship('UserModel', uselist=False, backref=backref('organization_managed', uselist=False))
    # contact = relationship('UserModel', uselist=False, backref=backref('organization_contact', uselist=False))
    branches = relationship('BranchModel', back_populates='organization',
                            foreign_keys='BranchModel.organization_id')

    super_manager = relationship('UserModel', foreign_keys=[
        super_manager_id], back_populates='supermanaged_organizations')
    manager = relationship('UserModel', foreign_keys=[
        manager_id], back_populates='managed_organizations')
