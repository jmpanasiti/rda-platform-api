import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from ...dependencies.auth_dependencies import has_permissions
from app.controller.organization_controller import OrganizationController
from app.core.enums.role_enum import ADMIN_ROLES
from app.core.enums.role_enum import ALL_ROLES
from app.core.enums.role_enum import role_list_to_str
from app.core.enums.role_enum import RoleEnum as Role
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.branch_schemas import BranchResponse
from app.schemas.organization_schemas import OrganizationRequest
from app.schemas.organization_schemas import OrganizationResponse
from app.schemas.token_schemas import DecodedJWT


router = APIRouter(prefix='/organizations')
router.responses = {
    500: se.InternalServerError.dict()
}

logger = logging.getLogger(__name__)
controller = OrganizationController()


@router.post(
    '/',
    status_code=201,
    responses={
        201: {'description': 'Organization created'},
        400: ce.BadRequest.dict(),
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Create a new organization',
)
async def create_organization(
    organization: OrganizationRequest,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> OrganizationResponse:
    return controller.create(organization)


@router.get(
    '/',
    responses={
        200: {'description': 'List of organizations availables'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='List of organizations',
)
async def list_organizations(
    limit: int = Query(ge=0, default=10),
    offset: int = Query(ge=0, default=0),
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> List[OrganizationResponse]:
    return controller.get_list_paginated(limit, offset)


@router.get(
    '/{org_id}',
    responses={
        200: {'description': ' Get Organization requested'},
        401: ce.Unauthorized.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Get one organization by id',
)
async def get_by_id(
    org_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ALL_ROLES)),
) -> OrganizationResponse:
    return controller.get_by_id(org_id)


@router.put(
    '/{org_id}',
    responses={
        200: {'description': 'Organization updated'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str([*ADMIN_ROLES, Role.supermanager])}',
    name='Update an organization by id',
)
async def update_org(
    org_id: UUID,
    org_data: OrganizationRequest,
    _: DecodedJWT = Depends(has_permissions(
        [*ADMIN_ROLES, Role.supermanager])),
) -> OrganizationResponse:
    return controller.update(org_id, org_data)


@router.delete(
    '/{org_id}',
    status_code=204,
    responses={
        204: {'description': 'Organization deleted'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str([Role.superadmin])}',
    name='Delete an organization by id',
)
async def delete_by_id(
    org_id: UUID,
    _: DecodedJWT = Depends(has_permissions([Role.superadmin])),
) -> None:
    return controller.delete(org_id)


@router.get(
    '/{org_id}/branches',
    responses={
        200: {'description': 'Organization updated'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Get organization\'s branches',
)
async def get_org_branches(
    org_id: UUID,
    _: DecodedJWT = Depends(has_permissions(
        [*ADMIN_ROLES])),
) -> List[BranchResponse]:
    return controller.get_org_branches(org_id)
