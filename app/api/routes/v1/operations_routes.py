from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Query
from fastapi import UploadFile
from fastapi.responses import FileResponse

from app.api.dependencies.auth_dependencies import has_permissions
from app.controller.operations_controller import OperationsController
from app.core.enums.role_enum import ADMIN_ROLES
from app.core.enums.role_enum import ALL_ROLES
from app.core.enums.role_enum import MANAGER_ROLES
from app.core.enums.role_enum import role_list_to_str
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.operations_schemas import OperationsRequestReq
from app.schemas.operations_schemas import OperationsRequestRes
from app.schemas.operations_schemas import OperationsRequestUpdateReq
from app.schemas.operations_schemas import OperationsSinisterReq
from app.schemas.operations_schemas import OperationsSinisterRes
from app.schemas.operations_schemas import OperationsSinisterUpdateReq
from app.schemas.token_schemas import DecodedJWT

router = APIRouter(prefix='/operations/{branch_id}')
router.responses = {
    500: se.InternalServerError.dict(),
    401: ce.Unauthorized.dict(),
    403: ce.Forbidden.dict(),
}
controller = OperationsController()

ALLOWED_ROLES = [*ADMIN_ROLES, *MANAGER_ROLES]


@router.get(
    '/requests',
    responses={
        200: {'description': 'Branch requests list'}
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Get branch requests list',
)
async def get_branch_requests(
        branch_id: UUID,
        limit: int = Query(ge=0, default=10),
        offset: int = Query(ge=0, default=0),
        _: DecodedJWT = Depends(has_permissions(ALL_ROLES))
) -> List[OperationsRequestRes]:
    return controller.get_requests_paginated(branch_id, limit, offset)


@router.post(
    '/requests',
    status_code=201,
    responses={
        201: {'description': 'Added a new branch request'}
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Add a new branch request',
)
async def add_new_branch_request(
    branch_id: UUID,
    request_data: OperationsRequestReq,
    _: DecodedJWT = Depends(has_permissions(ALL_ROLES)),
) -> OperationsRequestRes:
    return controller.add_new_request(branch_id, request_data)


@router.get(
    '/requests/{request_id}',
    responses={
        200: {'description': 'Branch request by ID'}
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Get branch request by ID',
)
async def get_one_branch_request(
        branch_id: UUID,
        request_id: UUID,
        _: DecodedJWT = Depends(has_permissions(ALL_ROLES)),

) -> OperationsRequestRes:
    return controller.get_request_by_id(branch_id, request_id)


@router.put(
    '/requests/{request_id}/approve',
    status_code=204,
    responses={
        204: {'description': 'Request setted as approved'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Approve a branch request',
)
async def approve_request(
        branch_id: UUID,
        request_id: UUID,
        token: DecodedJWT = Depends(has_permissions(ALL_ROLES)),

):
    approver_user_id = token.id
    return controller.approve_request(branch_id, request_id, approver_user_id)


@router.put(
    '/requests/{request_id}',
    responses={
        200: {'description': 'Branch request updated'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Update a branch request',
)
async def update_branch_requests(
    branch_id: UUID,
    request_id: UUID,
    request_data: OperationsRequestUpdateReq,
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),
) -> OperationsRequestRes:
    return controller.update_request(branch_id, request_id, request_data)


@router.delete(
    '/requests/{request_id}',
    status_code=204,
    responses={
        200: {'description': 'Branch request deleted'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Delete a branch request',
)
async def delete_branch_request(
    branch_id: UUID,
    request_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),
):
    return controller.delete_request(branch_id, request_id)


@router.post(
    '/requests/{request_id}/tires',
    status_code=204,
    responses={
        204: {'description': 'Files uploaded'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Upload files to a branch request',
)
async def upload_file(
    branch_id: UUID,
    request_id: UUID,
    file: UploadFile = File(...),
    _: DecodedJWT = Depends(has_permissions(ALL_ROLES)),
) -> None:
    return await controller.upload_request_file(branch_id, request_id, file)


@router.get(
    '/requests/{request_id}/tires/{file_name}',
    responses={
        200: {'description': 'File downloaded'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Upload files to a branch request',
)
async def download_file(
    branch_id: UUID,
    request_id: UUID,
    file_name: str,
    _: DecodedJWT = Depends(has_permissions(ALL_ROLES))
) -> FileResponse:
    return controller.download_request_file(branch_id, request_id, file_name)


@router.delete(
    '/requests/{request_id}/tires/{file_name}',
    status_code=204,
    responses={
        204: {'description': 'File deleted'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Upload files to a branch request',
)
async def delete_request_file_by_name(
    branch_id: UUID,
    request_id: UUID,
    file_name: str,
    _: DecodedJWT = Depends(has_permissions(ALL_ROLES))
) -> None:
    return controller.delete_request_file(branch_id, request_id, file_name)


@router.get(
    '/sinisters',
    responses={
        200: {'description': 'Branch sinisters list'}
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Get branch sinisters',
)
async def get_branch_sinisters(
        branch_id: UUID,
        limit: int = Query(ge=0, default=10),
        offset: int = Query(ge=0, default=0),
        _: DecodedJWT = Depends(has_permissions(ALL_ROLES))
) -> List[OperationsSinisterRes]:
    return controller.get_sinisters_paginated(branch_id, limit, offset)


@router.get(
    '/sinisters/{sinister_id}',
    responses={
        200: {'description': 'Branch sinister by ID'}
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Get branch sinisters',
)
async def get_one_branch_sinister(
        branch_id: UUID,
        sinister_id: UUID,
        _: DecodedJWT = Depends(has_permissions(ALL_ROLES)),

) -> OperationsSinisterRes:
    return controller.get_sinister_by_id(branch_id, sinister_id)


@router.post(
    '/sinisters',
    status_code=201,
    responses={
        201: {'description': 'Added a new sinister request'}
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Add a new sinister request',
)
async def add_new_branch_sinister(
    branch_id: UUID,
    sinister_data: OperationsSinisterReq,
    _: DecodedJWT = Depends(has_permissions(ALL_ROLES)),
) -> OperationsSinisterRes:
    return controller.add_new_sinister(branch_id, sinister_data)


@router.put(
    '/sinisters/{sinister_id}/approve',
    status_code=204,
    responses={
        204: {'description': 'Sinister setted as approved'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Approve a sinister request',
)
async def approve_sinister(
        branch_id: UUID,
        sinister_id: UUID,
        token: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),

) -> None:
    approver_user_id = token.id
    return controller.approve_sinister(branch_id, sinister_id, approver_user_id)


@router.put(
    '/sinisters/{sinister_id}',
    responses={
        200: {'description': 'Branch sinister updated'}
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Update a sinister request',
)
async def update_branch_sinister(
    branch_id: UUID,
    sinister_id: UUID,
    sinister_data: OperationsSinisterUpdateReq,
    _: DecodedJWT = Depends(has_permissions(ALL_ROLES)),
) -> OperationsSinisterRes:
    return controller.update_sinister(branch_id, sinister_id, sinister_data)


@router.delete(
    '/sinisters/{sinister_id}',
    status_code=204,
    responses={
        200: {'description': 'Branch sinister deleted'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Delete a sinister request',
)
async def delete_branch_sinister(
    branch_id: UUID,
    sinister_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),
):
    return controller.delete_sinister(branch_id, sinister_id)


@router.post(
    '/sinisters/{sinister_id}/files',
    status_code=204,
    responses={
        204: {'description': 'File uploaded'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Upload a sinister request',
)
async def upload_sinister_file(
    branch_id: UUID,
    sinister_id: UUID,
    file: UploadFile = File(...),
    _: DecodedJWT = Depends(has_permissions(ALL_ROLES)),
) -> None:
    return await controller.upload_sinister_file(branch_id, sinister_id, file)


@router.get(
    '/sinisters/{sinister_id}/files/{file_name}',
    responses={
        200: {'description': 'File downloaded'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Download a sinister request',
)
async def download_file_sinister(
    branch_id: UUID,
    sinister_id: UUID,
    file_name: str,
    _: DecodedJWT = Depends(has_permissions(ALL_ROLES))
) -> FileResponse:
    return controller.download_sinister_file(branch_id, sinister_id, file_name)


@router.delete(
    '/sinisters/{sinister_id}/files/{file_name}',
    status_code=204,
    responses={
        204: {'description': 'File deleted'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Delete a sinister request',
)
async def delete_sinister_file_by_name(
    branch_id: UUID,
    sinister_id: UUID,
    file_name: str,
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES))
) -> None:
    return controller.delete_sinister_file(branch_id, sinister_id, file_name)
