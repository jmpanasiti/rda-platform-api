from uuid import UUID

from ..database.models.user_model import UserModel
from ..repository.user_repository import UserRepository
from ..schemas.user_schemas import UserRequest
from ..schemas.user_schemas import UserResponse
from .base_service import BaseService


class UserService(BaseService[UserModel, UserRequest, UserResponse, UserRepository]):
    def __init__(self):
        super().__init__(UserRepository)

    # CRUD by default
    def get_by_username(self, username: str) -> UserResponse:
        return self._to_schema(self.repo.get_by_username(username))

    def activate(self, user_id: UUID) -> UserResponse:
        return self._to_schema(self.repo.activate(user_id))

    def deactivate(self, user_id: UUID) -> UserResponse:
        return self._to_schema(self.repo.deactivate(user_id))

    def _to_schema(self, user_model: UserModel | dict, method: str = '') -> UserResponse:
        if type(user_model) == dict:
            return UserResponse(**user_model)
        user_schema = UserResponse(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            phone=user_model.phone,
            job=user_model.job,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
            role=user_model.role,
            branch=user_model.branch,
            vehicle_id=user_model.vehicle_id,
            branch_id=user_model.branch_id,
            is_active=user_model.is_active,
            vehicle=user_model.vehicle,
            driver_license=user_model.driver_license,
        )
        return user_schema
