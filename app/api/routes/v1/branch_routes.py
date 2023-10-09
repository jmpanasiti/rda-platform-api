import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from ...dependencies.auth_dependencies import has_permissions
from app.controller.branch_controller import BranchController
from app.core.enums.role_enum import ADMIN_ROLES
from app.core.enums.role_enum import role_list_to_str
from app.core.enums.role_enum import RoleEnum as Role
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.branch_schemas import BranchRequest
from app.schemas.branch_schemas import BranchResponse
from app.schemas.token_schemas import DecodedJWT


router = APIRouter(prefix='/branches')
router.responses = {
    500: se.InternalServerError.dict()
}

logger = logging.getLogger(__name__)
controller = BranchController()


@router.post(
    '/',
    status_code=201,
    responses={
        201: {'description': 'Branch created'},
        400: ce.BadRequest.dict(),
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str([*ADMIN_ROLES, Role.supermanager])}',
    name='Create a new branch',
)
async def create_branch(
    branch: BranchRequest,
    token: DecodedJWT = Depends(has_permissions(
        [*ADMIN_ROLES, Role.supermanager]))
) -> BranchResponse:
    return controller.create(branch, token)


@router.get(
    '/',
    responses={
        200: {'description': 'List of branches availables'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str([*ADMIN_ROLES, Role.supermanager])}',
    name='List of branches',
)
async def list_branches(
    limit: int = Query(ge=0, default=10),
    offset: int = Query(ge=0, default=0),
    token: DecodedJWT = Depends(has_permissions(
        [*ADMIN_ROLES, Role.supermanager]))
) -> List[BranchResponse]:
    return controller.get_list_paginated(limit, offset, token)


@router.get(
    '/{branch_id}',
    responses={
        200: {'description': ' Get Branch requested'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Get one branch by id',
)
async def get_by_id(
    branch_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> BranchResponse:
    return controller.get_by_id(branch_id)


@router.put(
    '/{branch_id}',
    responses={
        200: {'description': 'Branch updated'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str([*ADMIN_ROLES, Role.supermanager])}',
    name='Update a branch by id',
)
async def update(
    branch_id: UUID,
    branch_data: BranchRequest,
    token: DecodedJWT = Depends(has_permissions(
        [*ADMIN_ROLES, Role.supermanager]))
) -> BranchResponse:
    return controller.update(branch_id, branch_data, token)


@router.delete(
    '/{branch_id}',
    status_code=204,
    responses={
        204: {'description': 'Branch deleted'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Delete a branch by id',
)
async def delete_by_id(
    branch_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> None:
    return controller.delete(branch_id)
