import logging
from uuid import UUID

from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.exceptions.repo_exceptions import BaseRepoException
from app.exceptions.repo_exceptions import NotFoundError
from app.repository.notification_repository import NotificationRepository
from app.schemas.notification_schemas import NotificationRequest

logger = logging.getLogger(__name__)


class NotificationService():
    def __init__(self) -> None:
        self.__notification_repo = None

    @property
    def notification_repo(self) -> NotificationRepository:
        if self.__notification_repo is None:
            self.__notification_repo = NotificationRepository()
        return self.__notification_repo

    def get_notifications(self, limit: int, offset: int):
        try:
            notifications = self.notification_repo.get_all(limit, offset)
            return notifications
        except Exception as ex:
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def create_notification(self, notification_data):
        try:
            new_notification = self.notification_repo.create({
                **notification_data.dict(),
            })
            return new_notification
        except BaseRepoException as ex:
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_notification_by_id(self, notification_id: UUID) -> NotificationRequest:
        try:
            notification = self.notification_repo.get_by_id(notification_id)
            return NotificationRequest.from_orm(notification)
        except NotFoundError as ex:
            logger.critical(ex.args)
            raise ce.NotFound('Notification not found.')

    def read_notification(self, notification_id: UUID):
        try:
            return self.notification_repo.update(notification_id, {
                'is_read': True,
            })
        except BaseRepoException as ex:
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def delete_notification(self, notification_id: UUID) -> None:
        try:
            return self.notification_repo.delete(notification_id)
        except BaseRepoException as ex:
            logger.critical(ex.args)
            raise se.InternalServerError(ex.args)

    def get_notification_by_filter(self, limit: int, offset: int, query):
        try:
            notifications = self.notification_repo.get_all(
                limit, offset, query)
            return notifications
        except Exception as ex:
            logger.critical(ex.args)
