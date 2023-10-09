from unittest import TestCase

from fastapi import status
from fastapi.testclient import TestClient

from .mocks.user_service_mocks import override_get_user_service
from app.app import app
from app.core.enums.role_enum import RoleEnum
from app.core.jwt import JWTManager
from app.service import get_user_service


class TestUserRoutes(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        app.dependency_overrides[get_user_service] = override_get_user_service
        cls.client = TestClient(app)
        cls.jwt_manager = JWTManager()

    def test_create(self):
        # Prepare test
        request_body = {
            'username': 'test_user',
            'password': 'test_password',
            'email': 'test_user@email.com',
            'role': 'agent',
            'first_name': 'Test',
            'last_name': 'User',
        }
        payload_jwt = {
            'id': 'f3df11ba-5daa-4659-b374-37d69c760714',
            'role': RoleEnum.admin.value,
        }
        headers = {
            'authorization': f'Bearer {self.jwt_manager.encode(payload_jwt)}'
        }

        # Run function to test
        response = self.client.post(
            '/api/v1/users', json=request_body, headers=headers)

        # Compare responses
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_unathorized(self):
        request_body = {
            'username': 'test_user',
            'password': 'test_password',
            'email': 'test_user@email.com',
            'role': 'agent',
            'first_name': 'Test',
            'last_name': 'User',
        }

        response = self.client.post(
            '/api/v1/users', json=request_body)  # Without token

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_forbidden(self):
        request_body = {
            'username': 'test_user',
            'password': 'test_password',
            'email': 'test_user@email.com',
            'role': 'agent',
            'first_name': 'Test',
            'last_name': 'User',
        }

        payload_jwt = {
            'id': 'f3df11ba-5daa-4659-b374-37d69c760714',
            'role': RoleEnum.agent.value,
        }
        headers = {
            'authorization': f'Bearer {self.jwt_manager.encode(payload_jwt)}'
        }

        response = self.client.post(
            '/api/v1/users', json=request_body, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all(self):
        payload_jwt = {
            'id': 'f3df11ba-5daa-4659-b374-37d69c760714',
            'role': RoleEnum.admin.value,
        }
        headers = {
            'authorization': f'Bearer {self.jwt_manager.encode(payload_jwt)}'
        }

        response = self.client.get('/api/v1/users', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_get_all_unauthorized(self):
        response = self.client.get('/api/v1/users')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_forbidden(self):
        payload_jwt = {
            'id': 'f3df11ba-5daa-4659-b374-37d69c760714',
            'role': RoleEnum.admin.agent,
        }
        headers = {
            'authorization': f'Bearer {self.jwt_manager.encode(payload_jwt)}'
        }

        response = self.client.get('/api/v1/users', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_by_id(self):
        payload_jwt = {
            'id': 'f3df11ba-5daa-4659-b374-37d69c760714',
            'role': RoleEnum.admin.value,
        }
        headers = {
            'authorization': f'Bearer {self.jwt_manager.encode(payload_jwt)}'
        }

        response = self.client.get(
            '/api/v1/users/f3df11ba-5daa-4659-b374-37d69c760714', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_id_not_found(self):
        payload_jwt = {
            'id': 'f3df11ba-5daa-4659-b374-37d69c760715',
            'role': RoleEnum.admin.value,
        }
        headers = {
            'authorization': f'Bearer {self.jwt_manager.encode(payload_jwt)}'
        }

        response = self.client.get(
            '/api/v1/users/f3df11ba-5daa-4659-b374-37d69c760715', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update(self):
        payload_jwt = {
            'id': 'f3df11ba-5daa-4659-b374-37d69c760714',
            'role': RoleEnum.admin.value,
        }
        headers = {
            'authorization': f'Bearer {self.jwt_manager.encode(payload_jwt)}'
        }
        request_body = {
            'username': 'test_user',
            'password': 'test_password',
            'email': 'test_user@email.com',
            'role': 'agent',
            'first_name': 'Test',
            'last_name': 'User',
        }

        response = self.client.put(
            '/api/v1/users/f3df11ba-5daa-4659-b374-37d69c760714', headers=headers, json=request_body)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        payload_jwt = {
            'id': 'f3df11ba-5daa-4659-b374-37d69c760714',
            'role': RoleEnum.admin.value,
        }
        headers = {
            'authorization': f'Bearer {self.jwt_manager.encode(payload_jwt)}'
        }
        response = self.client.delete(
            '/api/v1/users/f3df11ba-5daa-4659-b374-37d69c760714', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_error(self):
        payload_jwt = {
            'id': 'f3df11ba-5daa-4659-b374-37d69c760715',
            'role': RoleEnum.admin.value,
        }
        headers = {
            'authorization': f'Bearer {self.jwt_manager.encode(payload_jwt)}'
        }
        response = self.client.delete(
            '/api/v1/users/f3df11ba-5daa-4659-b374-37d69c760715', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_activate(self):
        payload_jwt = {
            'id': 'f3df11ba-5daa-4659-b374-37d69c760714',
            'role': RoleEnum.admin.value,
        }
        headers = {
            'authorization': f'Bearer {self.jwt_manager.encode(payload_jwt)}'
        }
        response = self.client.put(
            '/api/v1/users/f3df11ba-5daa-4659-b374-37d69c760714/activate', headers=headers)
        self.assertEqual(response.status_code, 204)

    def test_deactivate(self):
        payload_jwt = {
            'id': 'f3df11ba-5daa-4659-b374-37d69c760714',
            'role': RoleEnum.admin.value,
        }
        headers = {
            'authorization': f'Bearer {self.jwt_manager.encode(payload_jwt)}'
        }
        response = self.client.put(
            '/api/v1/users/f3df11ba-5daa-4659-b374-37d69c760714/deactivate', headers=headers)
        self.assertEqual(response.status_code, 204)
