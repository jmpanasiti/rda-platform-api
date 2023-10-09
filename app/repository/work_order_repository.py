import logging

from .base_repository import BaseRepository
from app.database.models.work_order_model import WorkOrderModel

logger = logging.getLogger(__name__)


class WorkOrderRepository(BaseRepository[WorkOrderModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = WorkOrderModel
