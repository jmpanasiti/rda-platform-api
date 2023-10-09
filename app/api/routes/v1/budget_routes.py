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
from app.controller.budget_controller import BudgetController
from app.core.enums.role_enum import ADMIN_ROLES
from app.core.enums.role_enum import role_list_to_str
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.budget_schemas import BudgetRequest
from app.schemas.budget_schemas import BudgetResponse
from app.schemas.token_schemas import DecodedJWT


router = APIRouter(prefix='/budgets')
router.responses = {
    500: se.InternalServerError.dict()
}

logger = logging.getLogger(__name__)
controller = BudgetController()


@router.post(
    '/',
    status_code=201,
    responses={
        201: {'description': 'Budget created'},
        400: ce.BadRequest.dict(),
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Create a new budget',
)
async def create_budget(
    budget_data: BudgetRequest,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> BudgetResponse:
    return controller.create(budget_data)


@router.get(
    '/',
    responses={
        200: {'description': 'List of budgets availables'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='List of budgets',
)
async def list_budgets(
    limit: int = Query(ge=0, default=10),
    offset: int = Query(ge=0, default=0),
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES))
) -> List[BudgetResponse]:
    return controller.get_list_paginated(limit, offset)


@router.get(
    '/{budget_id}',
    responses={
        200: {'description': ' Get Budget requested'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Get one budget by id',
)
async def get_by_id(
    budget_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> BudgetResponse:
    return controller.get_by_id(budget_id)


@router.put(
    '/{budget_id}',
    responses={
        200: {'description': 'Budget updated'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Update a budget by id',
)
async def update(
    budget_id: UUID,
    budget_data: BudgetRequest,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> BudgetResponse:
    return controller.update(budget_id, budget_data)


@router.delete(
    '/{budget_id}',
    status_code=204,
    responses={
        204: {'description': 'Budget deleted'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Delete a budget by id',
)
async def delete_by_id(
    budget_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> None:
    return controller.delete(budget_id)


@router.post(
    '/{budget_id}/upload',
    status_code=204,
    responses={
        204: {'description': 'Budget file uploaded'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Delete a budget by id',
)
async def upload_file(
    budget_id: UUID,
    file: UploadFile = File(...),
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> None:
    return await controller.upload_allocation_file(budget_id, file)


@router.get(
    '/{budget_id}/download',
    responses={
        200: {'description': 'Budget downloaded'},
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
        404: ce.NotFound.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ADMIN_ROLES)}',
    name='Delete a budget by id',
)
async def download_file(
    budget_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ADMIN_ROLES)),
) -> FileResponse:
    return controller.download_budget(budget_id)
