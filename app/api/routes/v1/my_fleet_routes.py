from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from app.api.dependencies.auth_dependencies import has_permissions
from app.controller.my_fleet_controller import MyFleetController
from app.core.enums.role_enum import ADMIN_ROLES
from app.core.enums.role_enum import ALL_ROLES
from app.core.enums.role_enum import MANAGER_ROLES
from app.core.enums.role_enum import role_list_to_str
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.my_fleet_schemas import MyFleetUserReq
from app.schemas.my_fleet_schemas import MyFleetUserRes
from app.schemas.my_fleet_schemas import MyFleetUserUpdateReq
from app.schemas.my_fleet_schemas import MyFleetVehicleReq
from app.schemas.my_fleet_schemas import MyFleetVehicleRes
from app.schemas.my_fleet_schemas import MyFleetVehicleUpdateReq
from app.schemas.token_schemas import DecodedJWT

router = APIRouter(prefix='/my-fleet/{branch_id}')
router.responses = {
    500: se.InternalServerError.dict(),
    401: ce.Unauthorized.dict(),
    403: ce.Forbidden.dict(),
}
controller = MyFleetController()

ALLOWED_ROLES = [*ADMIN_ROLES, *MANAGER_ROLES]


@router.get(
    '/vehicles',
    responses={
        200: {'description': 'Branch vehicle list'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Get fleet vehicles'
)
async def get_fleet_vehicles(
    branch_id: UUID,
    limit: int = Query(ge=0, default=10),
    offset: int = Query(ge=0, default=0),
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES))
) -> List[MyFleetVehicleRes]:
    return controller.get_vehicles_paginated(limit, offset, branch_id)


@router.get(
    '/vehicles/{vehicle_id}',
    responses={
        200: {'description': 'Branch vehicle by ID'}
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Get one fleet vehicle'
)
async def get_one_fleet_vehicle(
    branch_id: UUID,
    vehicle_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ALL_ROLES)),

) -> MyFleetVehicleRes:
    return controller.get_vehicle_by_id(branch_id, vehicle_id)


@router.post(
    '/vehicles',
    status_code=201,
    responses={
        201: {'description': 'Added a new branch vehicle'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Add a new fleet vehicle'
)
async def add_new_branch_vehicle(
    branch_id: UUID,
    vehicle_data: MyFleetVehicleReq,
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),
) -> MyFleetVehicleRes:
    return controller.add_new_vehicle(branch_id, vehicle_data)


@router.put(
    '/vehicles/{vehicle_id}',
    responses={
        200: {'description': 'Branch vehicle updated'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Update a fleet vehicle'
)
async def update_branch_vehicle(
    branch_id: UUID,
    vehicle_id: UUID,
    vehicle_data: MyFleetVehicleUpdateReq,
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),
) -> MyFleetVehicleRes:
    return controller.update_vehicle(branch_id, vehicle_id, vehicle_data)


@router.delete(
    '/vehicles/{vehicle_id}',
    status_code=204,
    responses={
        200: {'description': 'Branch vehicle deleted'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Update a fleet vehicle'
)
async def delete_branch_vehicle(
    branch_id: UUID,
    vehicle_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),
):
    return controller.delete_vehicle(branch_id, vehicle_id)


@router.put(
    '/vehicles/{vehicle_id}/activate',
    status_code=204,
    responses={
        200: {'description': 'Branch vehicle setted as active'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Activate a fleet vehicle',
)
async def activate_branch_vehicle(
    branch_id: UUID,
    vehicle_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),
):
    return controller.activate_vehicle(branch_id, vehicle_id)


@router.put(
    '/vehicles/{vehicle_id}/deactivate',
    status_code=204,
    responses={
        200: {'description': 'Branch vehicle setted as deactive'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Activate a fleet vehicle'
)
async def deactivate_branch_vehicle(
    branch_id: UUID,
    vehicle_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),
):
    return controller.deactivate_vehicle(branch_id, vehicle_id)


@router.get(
    '/users',
    responses={
        200: {'description': 'Branch user list'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='List of fleet users',
)
async def get_fleet_users(
    branch_id: UUID,
    limit: int = Query(ge=0, default=10),
    offset: int = Query(ge=0, default=0),
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES))
) -> List[MyFleetUserRes]:
    return controller.get_users_paginated(limit, offset, branch_id)


@router.get(
    '/users/{user_id}',
    responses={
        200: {'description': 'Branch user by ID'}
    },
    description=f'Authorized roles: {role_list_to_str(ALL_ROLES)}',
    name='Get one fleet user',
)
async def get_one_fleet_user(
    branch_id: UUID,
    user_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ALL_ROLES)),

) -> MyFleetUserRes:
    return controller.get_user_by_id(branch_id, user_id)


@router.post(
    '/users',
    status_code=201,
    responses={
        201: {'description': 'Added a new branch user'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Add a new fleet user',
)
async def add_new_branch_user(
    branch_id: UUID,
    user_data: MyFleetUserReq,
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),
) -> MyFleetUserRes:
    return controller.add_new_user(branch_id, user_data)


@router.put(
    '/users/{user_id}',
    responses={
        200: {'description': 'Branch user updated'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Update a fleet user',
)
async def update_branch_user(
    branch_id: UUID,
    user_id: UUID,
    user_data: MyFleetUserUpdateReq,
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),
) -> MyFleetUserRes:
    return controller.update_user(branch_id, user_id, user_data)


@router.delete(
    '/users/{user_id}',
    status_code=204,
    responses={
        200: {'description': 'Branch user deleted'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Delete a fleet user',
)
async def delete_branch_user(
    branch_id: UUID,
    user_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),
):
    return controller.delete_user(branch_id, user_id)


@router.put(
    '/users/{user_id}/activate',
    status_code=204,
    responses={
        200: {'description': 'Branch user setted as active'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Activate a fleet user',
)
async def activete_branch_user(
    branch_id: UUID,
    user_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),
):
    return controller.activate_user(branch_id, user_id)


@router.put(
    '/users/{user_id}/deactivate',
    status_code=204,
    responses={
        200: {'description': 'Branch user setted as deactive'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Activate a fleet user',
)
async def deactivate_branch_user(
    branch_id: UUID,
    user_id: UUID,
    _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),
):
    return controller.deactivate_user(branch_id, user_id)
