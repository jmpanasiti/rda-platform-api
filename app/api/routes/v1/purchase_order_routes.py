import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from ...dependencies.auth_dependencies import has_permissions
from app.controller.purchase_order_controller import PurchaseOrderController
from app.core.enums.role_enum import ADMIN_ROLES
from app.core.enums.role_enum import role_list_to_str
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.purchase_order_schemas import PurchaseOrderRequest
from app.schemas.purchase_order_schemas import PurchaseOrderResponse
from app.schemas.token_schemas import DecodedJWT


router = APIRouter(prefix='/purchase_orders')
router.responses = {
    500: se.InternalServerError.dict()
}

logger = logging.getLogger(__name__)
controller = PurchaseOrderController()


@router.post(
    '/',
    status_code=201,
    responses={
        201: {'description': 'Purchase Order created'},
        400: ce.BadRequest.dict(),
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Create a new purchase_order',
)
async def create_purchase_order(
    purchase_order: PurchaseOrderRequest,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> PurchaseOrderResponse:
    return controller.create(purchase_order)


@router.get(
    '/',
    responses={
        200: {'description': 'List of purchase_orders availables'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='List of purchase_orders',
)
async def list_purchase_orders(
    limit: int = Query(ge=0, default=10),
    offset: int = Query(ge=0, default=0),
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> List[PurchaseOrderResponse]:
    return controller.get_list(limit, offset)


@router.get(
    '/{purchase_order_id}',
    responses={
        200: {'description': ' Get PurchaseOrder requested'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Get one purchase order by id',
)
async def get_by_id(
    purchase_order_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> PurchaseOrderResponse:
    return controller.get_by_id(purchase_order_id)


@router.put(
    '/{purchase_order_id}',
    responses={
        200: {'description': 'PurchaseOrder updated'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Update a purchase order by id',
)
async def update(
    purchase_order_id: UUID,
    purchase_order_data: PurchaseOrderRequest,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> PurchaseOrderResponse:
    return controller.update(purchase_order_id, purchase_order_data)


@router.delete(
    '/{purchase_order_id}',
    status_code=204,
    responses={
        204: {'description': 'PurchaseOrder deleted'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Delete a purchase order by id',
)
async def delete_by_id(
    purchase_order_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> None:
    return controller.delete(purchase_order_id)
