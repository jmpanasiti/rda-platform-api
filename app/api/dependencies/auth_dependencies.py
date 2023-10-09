from typing import List

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.core.enums.role_enum import RoleEnum as Role
from app.core.jwt import JWTManager
from app.exceptions.client_exceptions import Forbidden
from app.exceptions.client_exceptions import Unauthorized
from app.schemas.token_schemas import DecodedJWT

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


def has_permissions(allowed_roles: List[Role] = []):
    async def get_token_payload(
            authorization=Depends(oauth2_scheme),
            jwt_manager: JWTManager = Depends()
    ) -> DecodedJWT:
        try:
            payload = jwt_manager.decode(authorization)

            if len(allowed_roles) > 0 and payload['role'] not in [role.value for role in allowed_roles]:
                raise Forbidden('You have no access to this resource.')
            return DecodedJWT(**payload)
        except InvalidTokenError:
            raise Unauthorized(message="Invalid token")
    return get_token_payload
