import logging

from .base_repository import BaseRepository
from app.database.models.purchase_order_model import PurchaseOrderModel

logger = logging.getLogger(__name__)


class PurchaseOrderRepository(BaseRepository[PurchaseOrderModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = PurchaseOrderModel
