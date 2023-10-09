from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from app.api.dependencies.auth_dependencies import has_permissions
from app.controller.notification_controller import NotificationController
from app.core.enums.role_enum import ALL_ROLES
from app.core.enums.role_enum import role_list_to_str
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.notification_schemas import NotificationFilterRequest
from app.schemas.notification_schemas import NotificationRequest
from app.schemas.notification_schemas import NotificationResponse
from app.schemas.token_schemas import DecodedJWT

router = APIRouter(prefix='/notifications')
router.responses = {
    500: se.InternalServerError.dict(),
    401: ce.Unauthorized.dict(),
    403: ce.Forbidden.dict(),
}
controller = NotificationController()

ALLOWED_ROLES = [*ALL_ROLES]


@router.post(
    '/',
    status_code=201,
    responses={
        201: {'description': 'Notification created'},
        400: ce.BadRequest.dict(),
        401: ce.Unauthorized.dict(),
        403: ce.Forbidden.dict(),
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Create a new notification',
)
async def create_notification(
        notification_data: NotificationRequest,
        _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES))
) -> NotificationResponse:
    return controller.create_notification(notification_data)


@router.get(
    '/',
    responses={
        200: {'description': 'Notifications list'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Get notifications',
)
async def get_notifications(
        limit: int = Query(ge=0, default=10),
        offset: int = Query(ge=0, default=0),
        _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES))
) -> List[NotificationResponse]:
    return controller.get_notifications_paginated(limit, offset)


@router.get(
    '/{notification_id}',
    responses={
        200: {'description': 'Notification by Vehicle ID'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Get notification by id',
)
async def get_notification_by_id(
        notification_id: UUID,
        _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),

) -> NotificationRequest:
    return controller.get_notification_by_id(notification_id)


@router.post(
    '/filter',
    responses={
        200: {'description': 'Notification by Vehicle ID'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Get notification filtered',
)
async def get_notification_filtered(
        filter: NotificationFilterRequest,
        limit: int = Query(ge=0, default=10),
        offset: int = Query(ge=0, default=0),
        _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),
) -> List[NotificationResponse]:
    return controller.get_notification_by_filter(limit, offset, filter)


@router.put(
    '/{notification_id}/read',
    responses={
        200: {'description': 'Notification Read'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Set notification as read',
)
async def read_notification(
        notification_id: UUID,
        _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),
) -> NotificationResponse:
    return controller.read_notification(notification_id)


@router.delete(
    '/{notification_id}',
    status_code=204,
    responses={
        200: {'description': 'Branch request deleted'}
    },
    description=f'Authorized roles: {role_list_to_str(ALLOWED_ROLES)}',
    name='Delete notification by id',
)
async def delete_notification(
        notification_id: UUID,
        _: DecodedJWT = Depends(has_permissions(ALLOWED_ROLES)),
):
    return controller.delete_notification(notification_id)
