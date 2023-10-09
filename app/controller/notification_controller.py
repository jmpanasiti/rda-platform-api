from typing import List
from uuid import UUID

from app.schemas.notification_schemas import NotificationRequest
from app.schemas.notification_schemas import NotificationResponse
from app.service.notification_service import NotificationService


class NotificationController():
    def __init__(self) -> None:
        self.__notification_service = None

    @property
    def notification_service(self) -> NotificationService:
        if self.__notification_service is None:
            self.__notification_service = NotificationService()
        return self.__notification_service

    def get_notifications_paginated(self, limit: int, offset: int) -> List[NotificationResponse]:
        notifications = self.notification_service.get_notifications(
            limit, offset)
        return notifications

    def create_notification(self, notification_data: NotificationRequest) -> NotificationResponse:
        return self.notification_service.create_notification(notification_data)

    def get_notification_by_id(self, notification_id: UUID) -> NotificationRequest:
        return self.notification_service.get_notification_by_id(notification_id)

    def read_notification(self, notification_id: UUID):
        return self.notification_service.read_notification(notification_id)

    def delete_notification(self, notification_id: UUID) -> None:
        return self.notification_service.delete_notification(notification_id)

    def get_notification_by_filter(self, limit: int, offset: int, filter):
        query = {}
        for field, value in filter.dict().items():
            if value is not None:
                query[field] = value
        return self.notification_service.get_notification_by_filter(limit, offset, query)
