import logging
from datetime import date
from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import Query
from fastapi import UploadFile
from fastapi.responses import FileResponse

from ...dependencies.auth_dependencies import has_permissions
from app.controller.user_controller import UserController
from app.core.enums.role_enum import ADMIN_ROLES
from app.core.enums.role_enum import ALL_ROLES
from app.core.enums.role_enum import role_list_to_str
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.driver_license_schemas import DriverLicenseResponse
from app.schemas.token_schemas import DecodedJWT
from app.schemas.user_schemas import FirstSuperAdmin
from app.schemas.user_schemas import UserRequest
from app.schemas.user_schemas import UserResponse
from app.schemas.user_schemas import UserUpdateRequest

router = APIRouter(prefix='/users')
router.responses = {
    500: se.InternalServerError.dict()
}

logger = logging.getLogger(__name__)

controller = UserController()


@router.post(
    '/',
    status_code=201,
    responses={
        201: {'description': 'User created'},
        400: ce.BadRequest.dict(),
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Create a new User',
)
async def create_user(
    user: UserRequest,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> UserResponse:
    return controller.create(user)


@router.post(
    '/first_superadmin',
    status_code=201,
    responses={
        201: {'description': 'User created'},
        400: ce.BadRequest.dict(),
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description='Authorized roles: not required',
    name='Create a the first superadmin',
)
async def create_default_superadmin(
    user: FirstSuperAdmin,
) -> UserResponse:
    return controller.create_default_superadmin(user)


@router.get(
    '/',
    responses={
        200: {'description': 'List of users'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='List of users',
)
async def list_users(
    limit: int = Query(ge=0, default=10),
    offset: int = Query(ge=0, default=0),
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> List[UserResponse]:
    return controller.get_list(limit, offset)


@router.get(
    '/{user_id}',
    responses={
        200: {'description': 'User requested'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Get one user by id',
)
async def get_by_id(
    user_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> UserResponse:
    try:
        return controller.get_by_id(user_id)
    except ce.NotFound as ex:
        raise ex


@router.put(
    '/{user_id}',
    responses={
        200: {'description': 'User updated'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Update a user by id',
)
async def update_user(
    user_id: UUID,
    user_data: UserUpdateRequest,
    token: dict = Depends(has_permissions(ALL_ROLES)),
) -> UserResponse:
    return controller.update(token, user_id, user_data)


@router.delete(
    '/{user_id}',
    status_code=204,
    responses={
        204: {'description': 'User deleted'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Delete a user by id',
)
async def delete_by_id(
    user_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> None:
    return controller.delete(user_id)


@router.put(
    '/{user_id}/activate',
    status_code=204,
    responses={
        204: {'description': 'User account setted as active'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Set a user account as active',
)
async def activate_user_account(
    user_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> None:
    return controller.activate(user_id)


@router.put(
    '/{user_id}/deactivate',
    status_code=204,
    responses={
        204: {'description': 'User account setted as deactive'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Set a user account as deactive',
)
async def deactivate_user_account(
    user_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> None:
    return controller.deactivate(user_id)


# ! DRIVER LICENSE
@router.post(
    '/{user_id}/driver-licenses',
    status_code=201,
    responses={
        201: {'description': 'File uploaded'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Upload a driver license file for a user.',
)
async def upload_driver_license(
    user_id: UUID,
    expiration_date: date = Form(...),
    file: UploadFile = File(...),
    token: DecodedJWT = Depends(has_permissions(ALL_ROLES)),
) -> DriverLicenseResponse:
    if user_id != token.id:
        raise ce.Forbidden('You have no access to upload this document.')
    return await controller.upload_license(user_id, expiration_date, file)


@router.get(
    '/{user_id}/driver-licenses/{license_id}/download',
    responses={
        200: {'description': 'File downloaded'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Download a user\'s driver license file',
)
async def download_license(
    user_id: UUID,
    license_id: UUID,
    token: DecodedJWT = Depends(has_permissions(ALL_ROLES)),
) -> FileResponse:
    if user_id != token.id:
        raise ce.Forbidden('You have no access to upload this document.')
    return controller.download_license(license_id)


@router.get(
    '/{user_id}/driver-licenses/{license_id}',
    responses={
        200: {'description': 'Driver license requested'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Get users\'s driver license data',
)
async def get_driver_license_data(
    user_id: UUID,
    license_id: UUID,
    token: DecodedJWT = Depends(has_permissions(ALL_ROLES)),
) -> DriverLicenseResponse:
    if user_id != token.id:
        raise ce.Forbidden('You have no access to upload this document.')
    return controller.get_license_data(license_id)
