from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from app.api.dependencies.auth_dependencies import has_permissions
from app.controller.my_bills_controller import MyBillsController
from app.core.enums.role_enum import ADMIN_ROLES
from app.core.enums.role_enum import MANAGER_ROLES
from app.core.enums.role_enum import role_list_to_str
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.my_bills_schemas import MyBillsPOReq
from app.schemas.my_bills_schemas import MyBillsPORes
from app.schemas.my_bills_schemas import MyBillsPOUpdateReq
from app.schemas.token_schemas import DecodedJWT

router = APIRouter(prefix='/my_bills/{branch_id}')
router.responses = {
    500: se.InternalServerError.dict(),
    401: ce.Unauthorized.dict(),
    403: ce.Forbidden.dict(),
}

controller = MyBillsController()

ALLOWED_ROLES = [*ADMIN_ROLES, *MANAGER_ROLES]


@router.get(
    '/purchase_orders',
    responses={
        200: {'description': 'Branch PO list'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Get branch purchase orders',
)
async def get_branch_purchase_orders(
    branch_id: UUID,
    limit: int = Query(ge=0, default=10),
    offset: int = Query(ge=0, default=0),
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES))
) -> List[MyBillsPORes]:
    return controller.get_po_paginated(limit, offset, branch_id)


@router.get(
    '/purchase_orders/{purchase_order_id}',
    responses={
        200: {'description': 'Branch PO by ID'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Get branch purchase order by id',
)
async def get_one_purchase_order(
    branch_id: UUID,
    purchase_order_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),

) -> MyBillsPORes:
    return controller.get_po_by_id(branch_id, purchase_order_id)


@router.post(
    '/purchase_orders',
    status_code=201,
    responses={
        201: {'description': 'Added a new branch PO'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Add a new branch purchase order',
)
async def add_new_purchase_order(
    branch_id: UUID,
    purchase_order_data: MyBillsPOReq,
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),
) -> MyBillsPORes:
    return controller.add_new_po(branch_id, purchase_order_data)


@router.put(
    '/purchase_orders/{purchase_order_id}',
    responses={
        200: {'description': 'Branch PO updated'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Update a branch purchase order',
)
async def update_purchase_order(
    branch_id: UUID,
    purchase_order_id: UUID,
    purchase_order_data: MyBillsPOUpdateReq,
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),
) -> MyBillsPORes:
    return controller.update_po(branch_id, purchase_order_id, purchase_order_data)


@router.delete(
    '/purchase_orders/{purchase_order_id}',
    status_code=204,
    responses={
        200: {'description': 'Branch PO deleted'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Delete a branch purchase order',
)
async def delete_purchase_order(
    branch_id: UUID,
    purchase_order_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),
):
    return controller.delete_po(branch_id, purchase_order_id)
