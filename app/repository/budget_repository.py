import logging

from .base_repository import BaseRepository
from app.database.models.budget_model import BudgetModel

logger = logging.getLogger(__name__)


class BudgetRepository(BaseRepository[BudgetModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = BudgetModel
