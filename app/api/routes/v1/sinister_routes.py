import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Query
from fastapi import UploadFile
from fastapi.responses import FileResponse

from ...dependencies.auth_dependencies import has_permissions
from app.controller.sinister_controller import SinisterController
from app.core.enums.role_enum import ADMIN_ROLES
from app.core.enums.role_enum import ALL_ROLES
from app.core.enums.role_enum import role_list_to_str
from app.core.enums.role_enum import RoleEnum as Role
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.sinister_schemas import SinisterRequest
from app.schemas.sinister_schemas import SinisterResponse
from app.schemas.token_schemas import DecodedJWT


router = APIRouter(prefix='/sinisters')
router.responses = {
    500: se.InternalServerError.dict()
}

logger = logging.getLogger(__name__)
controller = SinisterController()


@router.post(
    '/',
    status_code=201,
    responses={
        201: {'description': 'Sinister created'},
        400: ce.BadRequest.dict(),
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Create a new sinister',
)
async def create_sinister(
    sinister: SinisterRequest,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> SinisterResponse:
    return controller.create(sinister)


@router.get(
    '/',
    responses={
        200: {'description': 'List of sinisters availables'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='List of sinisters',
)
async def list_sinisters(
    limit: int = Query(ge=0, default=10),
    offset: int = Query(ge=0, default=0),
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> List[SinisterResponse]:
    return controller.get_list_paginated(limit, offset)


@router.get(
    '/{id}',
    responses={
        200: {'description': ' Get Sinister requested'},
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Get one sinister by id',
)
async def get_by_id(
    id: UUID,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> SinisterResponse:
    return controller.get_by_id(id)


@router.put(
    '/{id}',
    responses={
        200: {'description': 'Sinister updated'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str([*ADMIN_ROLES, Role.supermanager])}',
    name='Update a sinister by id',
)
async def update_sinister(
    id: UUID,
    sinister_data: SinisterRequest,
        _: DecodedJWT = Depends(has_permissions(
        [*ADMIN_ROLES, Role.supermanager])),
) -> SinisterResponse:
    return controller.update(id, sinister_data)


@router.delete(
    '/{id}',
    status_code=204,
    responses={
        204: {'description': 'Sinister deleted'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str([Role.superadmin])}',
    name='Delete a sinister by id',
)
async def delete_by_id(
    sinister_id: UUID,
    _: DecodedJWT = Depends(has_permissions([Role.superadmin])),
) -> None:
    return controller.delete(sinister_id)


# FILES
@router.post(
    '/{sinister_id}/files',
    status_code=204,
    responses={
        204: {'description': 'File uploaded'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Upload a file',
)
async def upload_file(
    sinister_id: UUID,
    file: UploadFile = File(...),
    _: DecodedJWT = Depends(has_permissions(ALL_ROLES)),
) -> None:
    return await controller.upload_file(sinister_id, file)


@router.get(
    '/{sinister_id}/files/{file_name}',
    responses={
        200: {'description': 'File downloaded'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Download a file',
)
async def download_file(
    sinister_id: UUID,
    file_name: str,
    _: DecodedJWT = Depends(has_permissions(ALL_ROLES))
) -> FileResponse:
    return controller.download_file(sinister_id, file_name)


@router.delete(
    '/{sinister_id}/files/{file_name}',
    status_code=204,
    responses={
        204: {'description': 'File deleted'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Delete a file',
)
async def delete_by_name(
    sinister_id: UUID,
    file_name: str,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> None:
    return controller.delete_file(sinister_id, file_name)
