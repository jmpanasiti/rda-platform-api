from datetime import datetime
from unittest import skipIf
from uuid import UUID

from sqlalchemy.exc import DataError
from sqlalchemy.exc import IntegrityError

from ..base.base_test_models import BaseTestModels
from ..utils.test_helpers import skip_db_test
from app.database.models.user_model import UserModel


class TestUserModel(BaseTestModels):
    def setUp(self) -> None:
        # Get DB session
        self.db_session = self.db.session

        # Delete table 'users' content
        self.db_session.query(UserModel).delete()
        self.db_session.commit()

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

    def tearDown(self) -> None:
        # Close connection
        self.db_session.close()

    @skipIf(skip_db_test, 'There are no test db present.')
    def test_create_user(self):
        user = UserModel(**self.user_1)
        self.db_session.add(user)
        self.db_session.commit()

        self.assertIsNotNone(user.id, 'must have a value')
        self.assertIsInstance(user.id, UUID, 'must be a UUID')
        self.assertIsInstance(user.created_at, datetime, 'must be a datetime')
        self.assertIsInstance(user.updated_at, datetime, 'must be a datetime')
        self.assertIsInstance(user.is_deleted, bool, 'must be a boolean')
        self.assertEqual(user.is_deleted, False, 'Initial state must be False')

    @skipIf(skip_db_test, 'There are no test db present')
    def test_unique_email(self):
        user_1 = UserModel(**self.user_1)
        self.db_session.add(user_1)
        self.db_session.commit()

        user_2 = UserModel(**self.user_2)
        user_2.email = user_1.email  # Set the same email
        self.db_session.add(user_2)
        with self.assertRaises(IntegrityError):
            self.db_session.commit()

    @skipIf(skip_db_test, 'There are no test db present')
    def test_unique_username(self):
        user_1 = UserModel(**self.user_1)
        self.db_session.add(user_1)
        self.db_session.commit()

        user_2 = UserModel(**self.user_2)
        user_2.username = user_1.username  # Set the same username
        self.db_session.add(user_2)
        with self.assertRaises(IntegrityError):
            self.db_session.commit()

    @skipIf(skip_db_test, 'There are no test db present')
    def test_empty_required_fields(self):
        user = UserModel(**self.user_1)
        with self.assertRaises(Exception):
            user.username = ''
        with self.assertRaises(Exception):
            user.email = ''
        with self.assertRaises(Exception):
            user.password = ''
        with self.assertRaises(Exception):
            user.first_name = ''
        with self.assertRaises(Exception):
            user.last_name = ''

    @skipIf(skip_db_test, 'There are no test db present')
    def test_invalid_email(self):
        user = UserModel(**self.user_1)
        with self.assertRaises(Exception):
            user.email = 'invalid_email'
        with self.assertRaises(Exception):
            user.email = 'invalid_email@'
        with self.assertRaises(Exception):
            user.email = 'invalid_email@some'
        with self.assertRaises(Exception):
            user.email = 'invalid_email@.com'

    @skipIf(skip_db_test, 'There are no test db present')
    def test_invalid_username(self):
        user = UserModel(**self.user_1)
        with self.assertRaises(Exception):
            user.username = 'invalid username'
        with self.assertRaises(Exception):
            user.username = '1nvalid_username'

    @skipIf(skip_db_test, 'There are no test db present')
    def test_invalid_role(self):
        user = UserModel(**self.user_1)
        user.role = 'some_weird'
        self.db_session.add(user)
        with self.assertRaises(DataError):
            self.db_session.commit()

    @skipIf(skip_db_test, 'There are no test db present')
    def test_updated_at(self):
        user = UserModel(**self.user_1)
        # Add user
        self.db_session.add(user)
        self.db_session.commit()

        old_updated_at = user.updated_at
        old_created_at = user.created_at
        old_uuid = user.id
        old_username = user.username

        # Update user
        user.username = 'change_something'
        self.db_session.add(user)
        self.db_session.commit()

        self.assertEqual(user.id, old_uuid)
        self.assertEqual(user.created_at, old_created_at)
        self.assertNotEqual(user.username, old_username)
        self.assertGreater(user.updated_at, old_updated_at)

    @skipIf(skip_db_test, 'There are no test db present')
    def test_string_fields_cannot_start_end_whitespaces(self):

        user = UserModel(**{
            'username': ' test_user_2 ',
            'password': 'test_password',
            'email': ' test_user_2@rda.com ',
            'first_name': ' Test ',
            'last_name': ' User ',
            'phone': ' +5492615000000 ',
            'job': ' Developer ',
            'role': 'admin',
        })
        self.db_session.add(user)
        self.db_session.commit()

        self.assertEqual(user.username, user.username.strip())
        self.assertEqual(user.email, user.email.strip())
        self.assertEqual(user.first_name, user.first_name.strip())
        self.assertEqual(user.last_name, user.last_name.strip())
        self.assertEqual(user.phone, user.phone.strip())
        self.assertEqual(user.job, user.job.strip())
