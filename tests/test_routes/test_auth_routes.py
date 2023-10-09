from unittest import TestCase

from fastapi.testclient import TestClient

from .mocks.auth_service_mocks import override_get_auth_service
from app.app import app
from app.exceptions.client_exceptions import Unauthorized
from app.service import get_auth_service


class TestAuthRoutes(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        app.dependency_overrides[get_auth_service] = override_get_auth_service
        cls.client = TestClient(app)

    def test_auth(self):
        credentials = {
            'username': 'test_user',
            'password': 'test_password',
        }

        response = self.client.post('/api/v1/auth/login', data=credentials)
        response_dict = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response_dict)
        self.assertIsInstance(response_dict['access_token'], str)
        self.assertIn('token_type', response_dict)
        self.assertEqual(response_dict['token_type'], 'bearer')

    def test_auth_error_username(self):
        credentials = {
            'username': 'wrong_username',
            'password': 'test_password',
        }

        response = self.client.post('/api/v1/auth/login', data=credentials)
        self.assertEqual(response.status_code, Unauthorized.status_code)

    def test_auth_error_password(self):
        credentials = {
            'username': 'test_user',
            'password': 'wrong_password',
        }

        response = self.client.post('/api/v1/auth/login', data=credentials)
        self.assertEqual(response.status_code, Unauthorized.status_code)
