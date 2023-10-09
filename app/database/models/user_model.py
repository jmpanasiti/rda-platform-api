import bcrypt
from pydantic import EmailStr
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from . import BaseModel
from ...core.enums.role_enum import RoleEnum


class UserModel(BaseModel):
    __tablename__ = 'users'

    username = Column(String(50), unique=True, index=True, nullable=False)
    _password = Column('password', String(60), nullable=False)
    email = Column(String(50), unique=True, index=True, nullable=False)
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(40), nullable=False)
    phone = Column(String(25), default='')
    job = Column(String(25), default='')
    is_active = Column(Boolean, default=True, nullable=False)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey(
        'vehicles.id'))

    role = Column(Enum(RoleEnum), nullable=False)

    branch_id = Column(UUID(as_uuid=True), ForeignKey('branches.id'))

    branch = relationship(
        'BranchModel', back_populates='users', foreign_keys=[branch_id])

    vehicle = relationship('VehicleModel', back_populates='users', foreign_keys=[
        vehicle_id])

    sinisters = relationship('SinisterModel', back_populates='user',
                             foreign_keys='SinisterModel.user_id')

    requests = relationship('RequestModel', back_populates='user',
                            foreign_keys='RequestModel.user_id')

    approved_requests = relationship('RequestModel', back_populates='approver_user',
                                     foreign_keys='RequestModel.approver_user_id')
    approved_sinisters = relationship('SinisterModel', back_populates='approver_user',
                                      foreign_keys='SinisterModel.approver_user_id')
    driver_license = relationship('DriverLicenseModel', back_populates='user')

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        self._password = hashed_password.decode('utf-8')

    @validates('email')
    def validate_email(self, key: str, email: str | None):
        if email is None:
            return email
        assert type(email) == str
        email = email.strip().lower()
        assert EmailStr.validate(email), 'Not a valid email address'
        return email

    @validates('username')
    def validate_username(self, key: str, username: str | None):
        if username is None:
            return username
        assert type(username) == str
        username = username.strip()

        assert len(
            username) >= 8, f'The {key} must be greater or equal than 8 characters'
        assert not username[0].isdigit()
        assert ' ' not in username
        return username

    @validates('password')
    def validate_password(self, key: str, password: str | None):
        if password is None:
            return password
        assert len(
            password) >= 8, f'The {key} must be greater or equal than 8 characters'
        return password

    @validates('first_name')
    def validate_first_name(self, key: str, first_name: str | None):
        if first_name is None:
            return first_name
        assert type(first_name) == str
        first_name = first_name.strip()
        assert len(
            first_name) > 0, f'The {key} can not be empty'
        return first_name

    @validates('last_name')
    def validate_last_name(self, key: str, last_name: str | None):
        if last_name is None:
            return last_name
        assert type(last_name) == str
        last_name = last_name.strip()
        assert len(
            last_name) > 0, f'The {key} can not be empty'
        return last_name

    @validates('phone')
    def validate_phone(self, key: str, phone: str | None):
        if phone is None:
            return phone
        assert type(phone) == str
        phone = phone.strip()
        return phone

    @validates('job')
    def validate_job(self, key: str, job: str | None):
        if job is None:
            return job
        assert type(job) == str
        job = job.strip()
        return job

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def __repr__(self) -> str:
        return f'<UserModel(id={self.id}, username={self.username}, email={self.email}, role={self.role})>'
