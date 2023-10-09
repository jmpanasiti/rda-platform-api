from datetime import datetime
from unittest import TestCase
from unittest.mock import patch
from uuid import UUID

from .mocks import user_repo_mocks as repo_mock
from app.service.user_service import UserModel
from app.service.user_service import UserRequest
from app.service.user_service import UserResponse
from app.service.user_service import UserService


class TestUserService(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.service = UserService()

        cls.user_1 = {
            'id': '71adb686-55a7-4d09-9610-08c4f341bb75',
            'username': 'test_user_1',
            'password': 'test_password',
            'email': 'test_user_1@rda.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '',
            'job': '',
            'role': 'admin',
            'is_active': True,
            'updated_at': datetime(2023, 4, 26, 16, 4, 47, 187571),
            'created_at': datetime(2023, 4, 26, 16, 4, 47, 187570),
            'is_deleted': False,
        }

    def test_to_schema(self):
        user_model = UserModel(**self.user_1)

        user_response = self.service._to_schema(user_model)

        self.assertIsInstance(user_response, UserResponse)
        self.assertIsInstance(user_response.id, UUID)
        self.assertIsInstance(user_response.username, str)
        self.assertIsInstance(user_response.email, str)
        self.assertIsInstance(user_response.first_name, str)
        self.assertIsInstance(user_response.last_name, str)
        self.assertIsInstance(user_response.phone, str)
        self.assertIsInstance(user_response.job, str)
        self.assertIsInstance(user_response.role, str)
        self.assertIsInstance(user_response.created_at, datetime)
        self.assertIsInstance(user_response.updated_at, datetime)

    def test_to_model(self):
        user_request = UserRequest(**self.user_1)

        user_model = self.service._to_model(user_request)

        self.assertIsInstance(user_model.id, UUID | None)
        self.assertIsInstance(user_model.username, str)
        self.assertIsInstance(user_model.password, str)
        self.assertIsInstance(user_model.email, str)
        self.assertIsInstance(user_model.first_name, str)
        self.assertIsInstance(user_model.last_name, str)
        self.assertIsInstance(user_model.phone, str)
        self.assertIsInstance(user_model.job, str)
        self.assertIsInstance(user_model.role, str)
        self.assertIsInstance(user_model.is_active, bool | None)
        self.assertIsInstance(user_model.is_deleted, bool | None)
        self.assertIsInstance(user_model.created_at, datetime | None)
        self.assertIsInstance(user_model.updated_at, datetime | None)

    @patch('app.repository.base_repository.BaseRepository.create', side_effect=repo_mock.create)
    def test_create(self, *args):
        user_request = UserRequest(**self.user_1)

        user_response = self.service.create(user_request)

        self.assertIsNotNone(user_response.id)
        self.assertIsInstance(user_response.id, UUID)
        self.assertIsInstance(user_response.created_at, datetime)
        self.assertIsInstance(user_response.updated_at, datetime)

    @patch('app.repository.base_repository.BaseRepository.get_by_id', side_effect=repo_mock.get_by_id)
    def test_get_one_by_id(self, *args):
        fake_id = '2a72a3c5-00e0-4c39-a882-05df27b3e202'

        user_response = self.service.get_by_id(fake_id)

        self.assertIsNotNone(user_response)
        self.assertIsInstance(user_response, UserResponse)
        self.assertIsNotNone(user_response.id)
        self.assertIsInstance(user_response.id, UUID)
        self.assertIsInstance(user_response.created_at, datetime)
        self.assertIsInstance(user_response.updated_at, datetime)

    @patch('app.repository.base_repository.BaseRepository.get_all', side_effect=repo_mock.get_all)
    def test_get_all(self, *args):
        limit_per_page = 20
        users_list = self.service.get_all(limit=limit_per_page, offset=0)

        self.assertIsNotNone(users_list)
        self.assertIsInstance(users_list, list)
        self.assertGreaterEqual(len(users_list), 0)
        self.assertLessEqual(len(users_list), limit_per_page)
        self.assertIsInstance(users_list[0], UserResponse)

    @patch('app.repository.base_repository.BaseRepository.update', side_effect=repo_mock.update)
    def test_update(self, *args):
        user_request = UserRequest(**self.user_1)
        fake_id = '2a72a3c5-00e0-4c39-a882-05df27b3e202'

        user_response = self.service.update(fake_id, user_request)

        self.assertIsNotNone(user_response)
        self.assertIsInstance(user_response, UserResponse)
        self.assertIsNotNone(user_response.id)
        self.assertIsInstance(user_response.id, UUID)
        self.assertIsInstance(user_response.created_at, datetime)
        self.assertIsInstance(user_response.updated_at, datetime)

    @patch('app.repository.base_repository.BaseRepository.delete', response=None)
    def test_delete(self, *args):
        fake_id = '2a72a3c5-00e0-4c39-a882-05df27b3e202'

        try:
            self.service.delete(fake_id)
            ok = True
        except Exception:
            ok = False
        self.assertTrue(ok, 'Deleted with errors')

    @patch('app.repository.user_repository.UserRepository.get_by_username', side_effect=repo_mock.get_by_username)
    def test_get_one_by_username(self, *args):
        fake_username = 'fake_user'

        user_response = self.service.get_by_username(fake_username)

        self.assertIsNotNone(user_response)
        self.assertIsInstance(user_response, UserResponse)
        self.assertIsNotNone(user_response.id)
        self.assertIsInstance(user_response.id, UUID)
        self.assertIsInstance(user_response.created_at, datetime)
        self.assertIsInstance(user_response.updated_at, datetime)

    @patch('app.repository.user_repository.UserRepository.activate', side_effect=repo_mock.activate)
    def test_activate(self, *args):
        fake_id = '2a72a3c5-00e0-4c39-a882-05df27b3e202'

        user_response = self.service.activate(fake_id)

        self.assertIsNotNone(user_response)
        self.assertIsInstance(user_response, UserResponse)
        self.assertIsNotNone(user_response.id)
        self.assertIsInstance(user_response.id, UUID)
        self.assertTrue(user_response.is_active)

    @patch('app.repository.user_repository.UserRepository.deactivate', side_effect=repo_mock.deactivate)
    def test_deactivate(self, *args):
        fake_id = '2a72a3c5-00e0-4c39-a882-05df27b3e202'

        user_response = self.service.deactivate(fake_id)

        self.assertIsNotNone(user_response)
        self.assertIsInstance(user_response, UserResponse)
        self.assertIsNotNone(user_response.id)
        self.assertIsInstance(user_response.id, UUID)
        self.assertFalse(user_response.is_active)
