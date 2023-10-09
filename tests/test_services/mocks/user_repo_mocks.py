from datetime import datetime
from uuid import UUID
from uuid import uuid4

from app.service.user_service import UserModel


def create(user_model: UserModel) -> UserModel:
    # BaseModel
    user_model.id = uuid4()
    user_model.is_deleted = False
    user_model.created_at = datetime.now()
    user_model.updated_at = datetime.now()

    # UserModel
    user_model.is_active = True


def get_by_id(id: UUID):
    user_model = UserModel()
    # BaseModel
    user_model.id = id
    user_model.is_deleted = False
    user_model.created_at = datetime.now()
    user_model.updated_at = datetime.now()

    # UserModel
    user_model.username = 'fake_user'
    user_model.password = 'fake_encripted_password'
    user_model.email = 'fake_user@email.com'
    user_model.first_name = 'Fake'
    user_model.last_name = 'User'
    user_model.phone = '+5491100000000'
    user_model.job = 'Developer'
    user_model.is_active = True
    user_model.role = 'manager'

    return user_model


def get_all(limit: int, _) -> list:
    user_list = []
    for _ in range(limit):
        user_list.append(get_by_id(uuid4()))

    return user_list


def update(user_model: UserModel, search_filter=None) -> dict:
    # BaseModel
    user_model.id = uuid4()
    user_model.is_deleted = False
    user_model.created_at = datetime.now()
    user_model.updated_at = datetime.now()

    # UserModel
    user_model.is_active = True
    return user_model.response_dict()


def get_by_username(username: str) -> UserModel:
    user_model = UserModel()
    # BaseModel
    user_model.id = uuid4()
    user_model.is_deleted = False
    user_model.created_at = datetime.now()
    user_model.updated_at = datetime.now()

    # UserModel
    user_model.username = username
    user_model.password = 'fake_encripted_password'
    user_model.email = 'fake_user@email.com'
    user_model.first_name = 'Fake'
    user_model.last_name = 'User'
    user_model.phone = '+5491100000000'
    user_model.job = 'Developer'
    user_model.is_active = True
    user_model.role = 'manager'

    return user_model


def activate(id: UUID):
    user_model = get_by_id(id)
    user_model.is_active = True
    return user_model


def deactivate(id: UUID):
    user_model = get_by_id(id)
    user_model.is_active = False
    return user_model
