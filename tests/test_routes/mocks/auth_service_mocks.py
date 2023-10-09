from app.core.jwt import jwt_manager
from app.exceptions.client_exceptions import Unauthorized
from app.schemas.auth_schemas import LoginSchema


class MockAuthService():
    def __init__(self, ) -> None:
        self.test_user = LoginSchema(
            username='test_user', password='test_password')

    def login(self, credentials: LoginSchema):
        if credentials.username == self.test_user.username and credentials.password == self.test_user.password:
            payload = {
                'id': 'some_id',
                'role': 'some_role',
            }
            return jwt_manager.encode(payload)
        raise Unauthorized('Error on username/password')


async def override_get_auth_service():
    return MockAuthService()
