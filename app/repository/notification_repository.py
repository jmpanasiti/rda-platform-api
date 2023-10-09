import logging

from .base_repository import BaseRepository
from app.database.models.notification_model import NotificationModel

logger = logging.getLogger(__name__)


class NotificationRepository(BaseRepository[NotificationModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = NotificationModel
