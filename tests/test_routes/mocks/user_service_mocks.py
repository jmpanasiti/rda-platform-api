from datetime import datetime
from typing import List
from uuid import UUID
from uuid import uuid4

from app.exceptions.client_exceptions import NotFound
from app.exceptions.repo_exceptions import NotFoundError
from app.schemas.user_schemas import UserRequest
from app.schemas.user_schemas import UserResponse
from app.service.user_service import UserService
# from app.core.jwt import jwt_manager
# from app.schemas.auth_schemas import LoginSchema


class MockUserService(UserService):
    def __init__(self, ) -> None:
        pass

    def create(self, user_request: UserRequest) -> UserResponse:
        return UserResponse(
            id=uuid4(),
            username=user_request.username,
            email=user_request.email,
            first_name=user_request.first_name,
            last_name=user_request.last_name,
            role=user_request.role,
            phone=user_request.phone,
            job=user_request.job,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def update(self, id: UUID, user_request: UserRequest) -> UserResponse:
        return UserResponse(
            id=id,
            username=user_request.username,
            email=user_request.email,
            first_name=user_request.first_name,
            last_name=user_request.last_name,
            role=user_request.role,
            phone=user_request.phone,
            job=user_request.job,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def get_all(self, limit: int = 10, offset: int = 0) -> List[UserResponse]:
        response = []

        for num in range(limit):
            response.append(UserResponse(
                id=uuid4(),
                username=f'test_user_{num+offset}',
                email=f'test_user_{num+offset}@mail.com',
                first_name=f'User {num+offset}',
                last_name='Test',
                role='agent',
                phone='',
                job='',
                is_active=True,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ))
        return response

    def get_by_id(self, id: UUID) -> UserResponse:
        id_ok = 'f3df11ba-5daa-4659-b374-37d69c760714'
        if str(id) != id_ok:
            raise NotFound(
                f'No resource was found in UserModel with the id "{id}"')
        return UserResponse(
            id=id,
            username='test_user',
            email='test_user@mail.com',
            first_name='Test',
            last_name='User',
            role='agent',
            phone='',
            job='',
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def get_by_username(self, username: str) -> UserResponse:
        username_ok = 'test_user'
        if username != username_ok:
            raise NotFoundError
        return UserResponse(
            id='f3df11ba-5daa-4659-b374-37d69c760714',
            username=username,
            email='test_user@mail.com',
            first_name='Test',
            last_name='User',
            role='agent',
            phone='',
            job='',
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def delete(self, id: UUID) -> None:
        id_ok = 'f3df11ba-5daa-4659-b374-37d69c760714'
        if str(id) != id_ok:
            raise NotFound(
                f'No resource was found in UserModel with the id "{id}"')

    def activate(self, user_id: UUID) -> UserResponse:
        id_ok = 'f3df11ba-5daa-4659-b374-37d69c760714'
        if str(user_id) != id_ok:
            raise NotFound(
                f'No resource was found in UserModel with the id "{id}"')
        return UserResponse(
            id=user_id,
            username='test_user',
            email='test_user@mail.com',
            first_name='Test',
            last_name='User',
            role='agent',
            phone='',
            job='',
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def deactivate(self, user_id: UUID) -> UserResponse:
        id_ok = 'f3df11ba-5daa-4659-b374-37d69c760714'
        if str(user_id) != id_ok:
            raise NotFound(
                f'No resource was found in UserModel with the id "{id}"')
        return UserResponse(
            id=user_id,
            username='test_user',
            email='test_user@mail.com',
            first_name='Test',
            last_name='User',
            role='agent',
            phone='',
            job='',
            is_active=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )


async def override_get_user_service():
    return MockUserService()
