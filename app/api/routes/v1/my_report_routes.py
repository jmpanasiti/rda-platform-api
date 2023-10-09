from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from app.api.dependencies.auth_dependencies import has_permissions
from app.controller.my_report_controller import MyReportController
from app.core.enums.role_enum import ADMIN_ROLES
from app.core.enums.role_enum import MANAGER_ROLES
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.my_report_schemas import MyReportSchema
from app.schemas.token_schemas import DecodedJWT


router = APIRouter(prefix='/my-report/{branch_id}')
router.responses = {
    500: se.InternalServerError.dict(),
    401: ce.Unauthorized.dict(),
    403: ce.Forbidden.dict(),
}
controller = MyReportController()

ALLOWED_ROLES = [*ADMIN_ROLES, *MANAGER_ROLES]


@router.get(
    '/vehicles',
    responses={
        200: {'description': 'List of active vehicles'}
    }
)
async def get_active_vehicles(
    branch_id: UUID,
    limit: int = Query(ge=0, default=10),
    offset: int = Query(ge=0, default=0),
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES))
) -> List[MyReportSchema]:
    return controller.get_active_vehicles(limit, offset, branch_id)


@router.get(
    '/vehicles_with_expenses',
    responses={
        200: {'description': 'List of vehicles with associated expenses'}
    }
)
async def get_vehicles_with_expenses(
    branch_id: UUID,
    vehicle_id: UUID,
    limit: int = Query(ge=0, default=10),
    offset: int = Query(ge=0, default=0),
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES))
) -> List[MyReportSchema]:
    return controller.get_vehicles_with_expenses(limit, offset, branch_id, vehicle_id)


@router.get(
    '/users_with_expenses',
    responses={
        200: {'description': 'List of users with associated expenses'}
    }
)
async def get_users_with_expenses(
    branch_id: UUID,
    user_id: UUID,
    limit: int = Query(ge=0, default=10),
    offset: int = Query(ge=0, default=0),
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES))
) -> List[MyReportSchema]:
    return controller.get_users_with_expenses(limit, offset, branch_id, user_id)
