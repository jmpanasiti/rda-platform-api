from unittest import skipIf
from uuid import UUID
from uuid import uuid4

from ..base.base_test_repos import BaseTestRepos
from ..utils.test_helpers import skip_db_test
from app.database.models.user_model import UserModel
from app.exceptions.repo_exceptions import NotFoundError
from app.repository.user_repository import UserRepository
# logger = test_helpers.get_logger(__name__)


class TestUserRepository(BaseTestRepos):
    def setUp(self) -> None:
        # self.db_session = self.db.session
        self.repo = UserRepository()
        self.repo.db = self.db.session

        # Delete table 'users' content
        self.repo.db.query(UserModel).delete()
        self.repo.db.commit()

        # Test users
        self.user_1 = {
            'username': 'test_user_1',
            'password': 'test_password',
            'email': 'test_user_1@rda.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '',
            'job': '',
            'role': 'admin',
        }
        self.user_2 = {
            'username': 'test_user_2',
            'password': 'test_password',
            'email': 'test_user_2@rda.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '',
            'job': '',
            'role': 'admin',
        }

    @skipIf(skip_db_test, 'There are no Test DB present.')
    def test_create(self):
        user = UserModel(**self.user_1)
        self.repo.create(user)

        self.assertIsNotNone(user.id)

    @skipIf(skip_db_test, 'There are no Test DB present.')
    def test_read_one_by_id(self):
        user_test = UserModel(**self.user_1)
        self.db.session.add(user_test)
        self.db.session.commit()

        user = self.repo.get_by_id(user_test.id)
        self.assertIsNotNone(user.id)
        self.assertIsInstance(user.id, UUID)
        self.assertEqual(user.id, user_test.id)

    @skipIf(skip_db_test, 'There are no Test DB present.')
    def test_read_non_existent_user_by_id(self):
        some_id = uuid4()

        with self.assertRaises(NotFoundError):
            self.repo.get_by_id(some_id)

    @skipIf(skip_db_test, 'There are no Test DB present.')
    def test_read_one_by_username(self):
        user_test = UserModel(**self.user_1)
        self.db.session.add(user_test)
        self.db.session.commit()

        user = self.repo.get_by_username(user_test.username)

        self.assertIsNotNone(user, 'User must be not None')
        self.assertEqual(user_test.username, user.username)
        self.assertIsInstance(user, UserModel)

    @skipIf(skip_db_test, 'There are no Test DB present.')
    def test_read_non_existent_user_by_username(self):
        with self.assertRaises(NotFoundError):
            self.repo.get_by_username('some_username')

    @skipIf(skip_db_test, 'There are no Test DB present.')
    def test_read_all(self):
        self.db.session.add(UserModel(**self.user_1))
        self.db.session.add(UserModel(**self.user_2))
        self.db.session.commit()

        users = self.repo.get_all()
        self.assertIsNotNone(users)
        self.assertGreater(len(users), 0)
        self.assertIsInstance(users, list)
        self.assertIsInstance(users[0], UserModel)

    @skipIf(skip_db_test, 'There are no Test DB present.')
    def test_read_all_paginated(self):
        self.db.session.add(UserModel(**self.user_1))
        self.db.session.add(UserModel(**self.user_2))
        self.db.session.commit()

        users_page_1 = self.repo.get_all(limit=1)
        self.assertIsNotNone(users_page_1)
        self.assertEqual(len(users_page_1), 1)
        self.assertIsInstance(users_page_1, list)
        self.assertIsInstance(users_page_1[0], UserModel)

        users_page_2 = self.repo.get_all(limit=1, offset=1)
        self.assertIsNotNone(users_page_2)
        self.assertEqual(len(users_page_2), 1)
        self.assertIsInstance(users_page_2, list)
        self.assertIsInstance(users_page_2[0], UserModel)

        self.assertNotEqual(users_page_1[0].id, users_page_2[0].id)

        users_page_3 = self.repo.get_all(limit=1, offset=2)
        self.assertIsNotNone(users_page_3)
        self.assertEqual(len(users_page_3), 0)
        self.assertIsInstance(users_page_3, list)

    @skipIf(skip_db_test, 'There are no Test DB present.')
    def test_update(self):
        user = UserModel(**self.user_1)
        self.db.session.add(user)
        self.db.session.commit()
        new_job = 'Developer'

        old_updated_at = user.updated_at
        old_uuid = user.id
        old_job = user.job

        user.job = new_job
        self.repo.update(user)

        self.assertEqual(user.id, old_uuid)
        self.assertEqual(user.job, new_job)
        self.assertGreater(user.updated_at, old_updated_at)
        self.assertNotEqual(user.job, old_job)

    @skipIf(skip_db_test, 'There are no Test DB present.')
    def test_update_non_existent_user(self):
        user = UserModel(**self.user_1)
        user.is_deleted = True
        self.db.session.add(user)
        self.db.session.commit()

        with self.assertRaises(NotFoundError):
            self.repo.update(user)

    @skipIf(skip_db_test, 'There are no Test DB present.')
    def test_delete(self):
        user = UserModel(**self.user_1)
        self.db.session.add(user)
        self.db.session.commit()

        self.repo.delete(user.id)

        self.assertTrue(user.is_deleted)

    @skipIf(skip_db_test, 'There are no Test DB present.')
    def test_delete_error(self):
        with self.assertRaises(NotFoundError):
            self.repo.delete(uuid4())

    @skipIf(skip_db_test, 'There are no Test DB present.')
    def test_get_deleted(self):
        user = UserModel(**self.user_1)
        self.db.session.add(user)
        self.db.session.commit()
        self.repo.delete(user.id)

        with self.assertRaises(NotFoundError):
            self.repo.delete(user.id)

    @skipIf(skip_db_test, 'There are no Test DB present.')
    def test_activate(self):
        user = UserModel(**self.user_1)
        user.is_active = False
        self.db.session.add(user)
        self.db.session.commit()
        self.repo.activate(user.id)

        self.assertTrue(user.is_active)

    @skipIf(skip_db_test, 'There are no Test DB present.')
    def test_deactivate(self):
        user = UserModel(**self.user_1)
        self.db.session.add(user)
        self.db.session.commit()
        self.repo.deactivate(user.id)

        self.assertFalse(user.is_active)
