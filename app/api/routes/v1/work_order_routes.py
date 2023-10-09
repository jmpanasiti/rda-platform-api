import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from ...dependencies.auth_dependencies import has_permissions
from app.controller.work_order_controller import WorkOrderController
from app.core.enums.role_enum import ADMIN_ROLES
from app.core.enums.role_enum import role_list_to_str
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.token_schemas import DecodedJWT
from app.schemas.work_order_schemas import WorkOrderRequest
from app.schemas.work_order_schemas import WorkOrderResponse


router = APIRouter(prefix='/work_orders')
router.responses = {
    500: se.InternalServerError.dict()
}

logger = logging.getLogger(__name__)
controller = WorkOrderController()


@router.post(
    '/',
    status_code=201,
    responses={
        201: {'description': 'Work order created'},
        400: ce.BadRequest.dict(),
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Create a new work order'
)
async def create_work_order(
    work_order: WorkOrderRequest,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> WorkOrderResponse:
    return controller.create(work_order)


@router.get(
    '/',
    responses={
        200: {'description': 'List of work orders availables'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='List of work orders'
)
async def list_work_orders(
    limit: int = Query(ge=0, default=10),
    offset: int = Query(ge=0, default=0),
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> List[WorkOrderResponse]:
    return controller.get_list_paginated(limit, offset)


@router.get(
    '/{work_order_id}',
    responses={
        200: {'description': ' Get work order requested'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Get one work order by id'
)
async def get_by_id(
    work_order_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> WorkOrderResponse:
    return controller.get_by_id(work_order_id)


@router.put(
    '/{work_order_id}',
    responses={
        200: {'description': 'Work order updated'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Update a work order by id'
)
async def update(
    work_order_id: UUID,
    work_order_data: WorkOrderRequest,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> WorkOrderResponse:
    return controller.update(work_order_id, work_order_data)


@router.delete(
    '/{work_order_id}',
    status_code=204,
    responses={
        204: {'description': 'Work Order deleted'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Delete a work order by id',
)
async def delete_by_id(
    work_order_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> None:
    return controller.delete(work_order_id)
