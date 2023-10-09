import logging

from .base_repository import BaseRepository
from app.database.models.branch_model import BranchModel

logger = logging.getLogger(__name__)


class BranchRepository(BaseRepository[BranchModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = BranchModel
