import logging

from .base_repository import BaseRepository
from app.database.models.organization_model import OrganizationModel

logger = logging.getLogger(__name__)


class OrganizationRepository(BaseRepository[OrganizationModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = OrganizationModel
