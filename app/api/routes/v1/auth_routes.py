import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from ...dependencies.auth_dependencies import has_permissions
from app.controller.auth_controller import AuthController
from app.core.enums.role_enum import ALL_ROLES
from app.core.enums.role_enum import role_list_to_str
from app.exceptions import client_exceptions as ce
from app.schemas.auth_schemas import LoginSchema
from app.schemas.auth_schemas import RegisterSchema
from app.schemas.auth_schemas import TokenResponse
from app.schemas.token_schemas import DecodedJWT
from app.schemas.user_schemas import UserResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/auth')
controller = AuthController()


@router.post(
    '/register',
    responses={
        201: {'description': 'New user, organization and main branch registered'},
        400: ce.BadRequest.dict(),
    },
    description='Authorized roles: not required',
    name='Register a user with his first organization and branch',
)
async def register(
        register_data: RegisterSchema,
) -> TokenResponse:
    return controller.register(register_data)


@router.post(
    '/login',
    responses={
        201: {'description': 'User loggedin'},
        401: ce.Unauthorized.dict(),
    },
    description='Authorized roles: not required',
    name='Login a user. Returns a token',
)
async def login(
        credentials: OAuth2PasswordRequestForm = Depends(),
) -> TokenResponse:
    return controller.login(
        LoginSchema(username=credentials.username,
                    password=credentials.password)
    )


@router.get(
    '/info',
    responses={
        201: {'description': 'User info'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Get current user info',
)
async def get_current_user_info(
    token: DecodedJWT = Depends(has_permissions(ALL_ROLES))
) -> UserResponse:
    return controller.get_current_user_info(token)


@router.get(
    '/token',
    responses={
        201: {'description': 'User loggedin'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Get a renewed token',
)
async def renew_token(
    token: DecodedJWT = Depends(has_permissions(ALL_ROLES))
) -> TokenResponse:
    return controller.renew_token(token)
