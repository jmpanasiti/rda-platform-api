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
from app.controller.vehicle_controller import VehicleController
from app.core.enums.role_enum import ADMIN_ROLES
from app.core.enums.role_enum import ALL_ROLES
from app.core.enums.role_enum import role_list_to_str
from app.core.enums.role_enum import RoleEnum as Role
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.token_schemas import DecodedJWT
from app.schemas.vehicle_schemas import VehicleRequest
from app.schemas.vehicle_schemas import VehicleResponse

router = APIRouter(prefix='/vehicles')
router.responses = {
    500: se.InternalServerError.dict()
}

logger = logging.getLogger(__name__)
controller = VehicleController()


@router.post(
    '/',
    status_code=201,
    responses={
        201: {'description': 'Vehicle created'},
        400: ce.BadRequest.dict(),
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Create a new vehicle',
)
async def create_vehicle(
        vehicle: VehicleRequest,
        _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> VehicleResponse:
    return controller.create(vehicle)


@router.get(
    '/',
    responses={
        200: {'description': 'List of vehicles available'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='List of vehicles',
)
async def list_vehicles(
        limit: int = Query(ge=0, default=10),
        offset: int = Query(ge=0, default=0),
        _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> List[VehicleResponse]:
    return controller.get_list_paginated(limit, offset)


@router.get(
    '/{vehicle_id}',
    responses={
        200: {'description': ' Get Vehicle requested'},
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Get one vehicle by id',
)
async def vehicle_id(
        vehicle_id: UUID,
        _: DecodedJWT = Depends(has_permissions(ALL_ROLES)),
) -> VehicleResponse:
    return controller.get_by_id(vehicle_id)


@router.put(
    '/{vehicle_id}',
    responses={
        200: {'description': 'Vehicle updated'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str([*ADMIN_ROLES, Role.supermanager])}',
    name='Update a vehicle by id',
)
async def update_vehicle(
        vehicle_id: UUID,
        vehicle_data: VehicleRequest,
        _: DecodedJWT = Depends(has_permissions(
            [*ADMIN_ROLES, Role.supermanager])),
) -> VehicleResponse:
    return controller.update(vehicle_id, vehicle_data)


@router.delete(
    '/{vehicle_id}',
    status_code=204,
    responses={
        204: {'description': 'Vehicle deleted'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str([Role.superadmin])}',
    name='Delete a vehicle by id',
)
async def delete_by_id(
        vehicle_id: UUID,
        _: DecodedJWT = Depends(has_permissions([Role.superadmin])),
) -> None:
    return controller.delete(vehicle_id)


@router.put(
    '/{vehicle_id}/activate',
    status_code=204,
    responses={
        204: {'description': 'Vehicle setted as active'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Set a vehicle account as active',
)
async def activate_vehicle(
        vehicle_id: UUID,
        _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> None:
    return controller.activate(vehicle_id)


@router.put(
    '/{vehicle_id}/deactivate',
    status_code=204,
    responses={
        204: {'description': 'Vehicle setted as deactive'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Set a vehicle account as deactive',
)
async def deactivate_vehicle(
        vehicle_id: UUID,
        _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> None:
    return controller.deactivate(vehicle_id)


@router.post(
    '/{vehicle_id}/policy',
    status_code=204,
    responses={
        204: {'description': 'policy file uploaded'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Upload policy file',
)
async def upload_file(
        vehicle_id: UUID,
        file: UploadFile = File(...),
        _: DecodedJWT = Depends(has_permissions(ALL_ROLES)),
) -> None:
    return await controller.upload_policy(vehicle_id, file)


@router.post(
    '/{vehicle_id}/idcard',
    status_code=204,
    responses={
        204: {'description': 'id card file uploaded'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Upload id card file',
)
async def upload_idcard(
        vehicle_id: UUID,
        file: UploadFile = File(...),
        _: DecodedJWT = Depends(has_permissions(ALL_ROLES)),
) -> None:
    return await controller.upload_idcard(vehicle_id, file)


@router.post(
    '/{vehicle_id}/auth_idcard',
    status_code=204,
    responses={
        204: {'description': 'auth id card file uploaded'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Upload authorization id card file',
)
async def upload_auth_idcard(
        vehicle_id: UUID,
        file: UploadFile = File(...),
        _: DecodedJWT = Depends(has_permissions(ALL_ROLES)),
) -> None:
    return await controller.upload_auth_idcard(vehicle_id, file)


@router.post(
    '/{vehicle_id}/title',
    status_code=204,
    responses={
        204: {'description': 'title file uploaded'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Upload title file',
)
async def upload_title(
        vehicle_id: UUID,
        file: UploadFile = File(...),
        _: DecodedJWT = Depends(has_permissions(ALL_ROLES)),
) -> None:
    return await controller.upload_title(vehicle_id, file)


@router.get(
    '/{vehicle_id}/policy/{file_name}',
    responses={
        200: {'description': 'File downloaded'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Download a vehicle\'s policy file',
)
async def download_policy(
        vehicle_id: UUID,
        file_name: str,
        _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> FileResponse:
    return controller.download_policy(vehicle_id, file_name)


@router.get(
    '/{vehicle_id}/idcard/{file_name}',
    responses={
        200: {'description': 'File downloaded'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Download a vehicle\'s id card file',
)
async def download_idcard(
        vehicle_id: UUID,
        file_name: str,
        _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> FileResponse:
    return controller.download_idcard(vehicle_id, file_name)


@router.get(
    '/{vehicle_id}/auth_idcard/{file_name}',
    responses={
        200: {'description': 'File downloaded'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Download a vehicle\'s authorization id card file',
)
async def download_auth_idcard(
        vehicle_id: UUID,
        file_name: str,
        _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> FileResponse:
    return controller.download_auth_idcard(vehicle_id, file_name)


@router.get(
    '/{vehicle_id}/title/{file_name}',
    responses={
        200: {'description': 'File downloaded'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Download a vehicle\'s title file',
)
async def download_title(
        vehicle_id: UUID,
        file_name: str,
        _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> FileResponse:
    return controller.download_title(vehicle_id, file_name)


@router.delete(
    '/{vehicle_id}/policy/{file_name}',
    status_code=204,
    responses={
        204: {'description': 'File deleted'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Delete a vehicle\'s policy file',
)
async def delete_policy(
        vehicle_id: UUID,
        file_name: str,
        _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> None:
    return controller.delete_policy(vehicle_id, file_name)


@router.delete(
    '/{vehicle_id}/idcard/{file_name}',
    status_code=204,
    responses={
        204: {'description': 'File deleted'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Delete a vehicle\'s id card file',
)
async def delete_idcard(
        vehicle_id: UUID,
        file_name: str,
        _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> None:
    return controller.delete_idcard(vehicle_id, file_name)


@router.delete(
    '/{vehicle_id}/auth_idcard/{file_name}',
    status_code=204,
    responses={
        204: {'description': 'File deleted'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Delete a vehicle\'s authorization id card file',
)
async def delete_auth_idcard(
        vehicle_id: UUID,
        file_name: str,
        _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> None:
    return controller.delete_auth_idcard(vehicle_id, file_name)


@router.delete(
    '/{vehicle_id}/title/{file_name}',
    status_code=204,
    responses={
        204: {'description': 'File deleted'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Delete a vehicle\'s title file',
)
async def delete_title(
        vehicle_id: UUID,
        file_name: str,
        _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> None:
    return controller.delete_title(vehicle_id, file_name)
