import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from ...dependencies.auth_dependencies import has_permissions
from app.controller.request_controller import RequestController
from app.core.enums.role_enum import ADMIN_ROLES
from app.core.enums.role_enum import role_list_to_str
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.request_schemas import ServiceRequestReq
from app.schemas.request_schemas import ServiceRequestRes
from app.schemas.token_schemas import DecodedJWT


router = APIRouter(prefix='/requests')
router.responses = {
    500: se.InternalServerError.dict()
}

logger = logging.getLogger(__name__)
controller = RequestController()


@router.post(
    '/',
    status_code=201,
    responses={
        201: {'description': 'Request created'},
        400: ce.BadRequest.dict(),
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Create a new request',
)
async def create_request(
    request: ServiceRequestReq,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> ServiceRequestRes:
    return controller.create(request)


@router.get(
    '/',
    responses={
        200: {'description': 'List of Requests availables'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='List of Requests',
)
async def list_requests(
    limit: int = Query(ge=0, default=10),
    offset: int = Query(ge=0, default=0),
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> List[ServiceRequestRes]:
    return controller.get_list_paginated(limit, offset)


@router.get(
    '/{request_id}',
    responses={
        200: {'description': ' Get Request requested'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Get one request by id',
)
async def get_by_id(
    request_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> ServiceRequestRes:
    return controller.get_by_id(request_id)


@router.put(
    '/{request_id}',
    responses={
        200: {'description': 'Request updated'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Update a request by id',
)
async def update(
    request_id: UUID,
    request_data: ServiceRequestReq,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> ServiceRequestRes:
    return controller.update(request_id, request_data)


@router.delete(
    '/{request_id}',
    status_code=204,
    responses={
        204: {'description': 'request deleted'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Delete a request by id',
)
async def delete_by_id(
    request_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> None:
    return controller.delete(request_id)
