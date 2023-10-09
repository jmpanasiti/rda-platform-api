from unittest import TestCase

from fastapi.testclient import TestClient

from app.app import app


class TestAppClient(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_read_main(self):
        response = self.client.get('/api/v1/test/')
        assert response.status_code == 200
