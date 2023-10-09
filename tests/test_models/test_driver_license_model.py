from unittest import skipIf

from sqlalchemy.exc import IntegrityError

from ..base.base_test_models import BaseTestModels
from ..utils.test_helpers import skip_db_test
from app.database.models.driver_license_model import DriverLicenseModel
from app.database.models.user_model import UserModel


class TestDriverLicenseModel(BaseTestModels):
    def setUp(self) -> None:
        # Get DB session
        self.db_session = self.db.session

        # Delete table 'driver_licenses' content
        self.db_session.query(DriverLicenseModel).delete()
        self.db_session.query(UserModel).delete()
        self.db_session.commit()

        # Test users
        self.user = UserModel(**{
            'username': 'test_user',
            'password': 'test_password',
            'email': 'test_user@rda.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '',
            'job': '',
            'role': 'admin',
        })
        self.db_session.add(self.user)
        self.db_session.commit()
        self.db_session.rollback()

    def tearDown(self) -> None:
        # Close connection
        self.db_session.close()

    @skipIf(skip_db_test, 'There are no test db present.')
    def test_create_driver_license(self):
        driver_license = DriverLicenseModel(
            expiration_date='2034-12-23',
            file_name='test_file.jpg',
            file_type='image/jpeg',
            user=self.user
        )
        self.db_session.add(driver_license)
        self.db_session.commit()

        self.assertIsNotNone(driver_license.id)
        self.assertIsNotNone(driver_license.user_id)
        self.assertIsNotNone(driver_license.user.id)
        self.assertEqual(driver_license.user.id, driver_license.user_id)

    @skipIf(skip_db_test, 'There are no test db present.')
    def test_create_driver_license_without_user(self):
        driver_license = DriverLicenseModel(
            expiration_date='2034-12-23',
            file_name='test_file.jpg',
            file_type='image/jpeg',
        )
        self.db_session.add(driver_license)
        with self.assertRaises(IntegrityError):
            self.db_session.commit()
