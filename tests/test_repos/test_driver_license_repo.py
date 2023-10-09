from unittest import skipIf
from uuid import UUID

from ..base.base_test_repos import BaseTestRepos
from ..utils.test_helpers import skip_db_test
from app.database.models.driver_license_model import DriverLicenseModel
from app.database.models.user_model import UserModel
from app.repository.driver_license_repository import DriverLicenseRepository
# logger = test_helpers.get_logger(__name__)


class TestDriverLicenseRepository(BaseTestRepos):
    def setUp(self) -> None:
        # self.db_session = self.db.session
        self.repo = DriverLicenseRepository()
        self.repo.db = self.db.session

        # Delete table 'users' content
        self.repo.db.query(DriverLicenseModel).delete()
        self.repo.db.query(UserModel).delete()
        self.repo.db.commit()

        # Test User
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
        self.repo.db.add(self.user)
        self.repo.db.commit()

        # Test license data
        self.license = {
            'expiration_date': '2034-12-23',
            'file_name': 'test_file.jpg',
            'file_type': 'image/jpeg',
        }

    @skipIf(skip_db_test, 'There are no Test DB present.')
    def test_create(self):
        driver_license = DriverLicenseModel(**self.license)
        driver_license.user = self.user

        self.repo.create(driver_license)

        self.assertIsNotNone(driver_license.id)

    @skipIf(skip_db_test, 'There are no Test DB present.')
    def test_read_one(self):
        driver_license_test = DriverLicenseModel(
            **self.license
        )
        driver_license_test.user_id = self.user.id
        self.db.session.add(driver_license_test)
        self.db.session.commit()

        driver_license = self.repo.get_by_id(driver_license_test.id)
        self.assertIsNotNone(driver_license.id)
        self.assertIsInstance(driver_license.id, UUID)
        self.assertEqual(driver_license.id, driver_license_test.id)

    @skipIf(skip_db_test, 'There are no Test DB present.')
    def test_update(self):
        driver_license = DriverLicenseModel(
            **self.license
        )
        driver_license.user_id = self.user.id
        self.db.session.add(driver_license)
        self.db.session.commit()

        new_filename = 'new_filename.jpg'

        old_updated_at = driver_license.updated_at
        old_uuid = driver_license.id
        old_filename = driver_license.file_name

        driver_license.file_name = new_filename
        self.repo.update(driver_license)

        self.assertEqual(driver_license.id, old_uuid)
        self.assertEqual(driver_license.file_name, new_filename)
        self.assertGreater(driver_license.updated_at, old_updated_at)
        self.assertNotEqual(driver_license.file_name, old_filename)

    @skipIf(skip_db_test, 'There are no Test DB present.')
    def test_delete(self):
        driver_license = DriverLicenseModel(
            **self.license
        )
        driver_license.user_id = self.user.id
        self.db.session.add(driver_license)
        self.db.session.commit()

        self.repo.delete(driver_license.id)

        self.assertTrue(driver_license.is_deleted)
