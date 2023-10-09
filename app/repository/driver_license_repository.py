import logging

from .base_repository import BaseRepository
from app.database.models.driver_license_model import DriverLicenseModel

logger = logging.getLogger(__name__)


class DriverLicenseRepository(BaseRepository[DriverLicenseModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = DriverLicenseModel
