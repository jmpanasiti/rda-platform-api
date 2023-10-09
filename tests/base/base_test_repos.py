from .base_test_models import BaseTestModels


class BaseTestRepos(BaseTestModels):
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()
