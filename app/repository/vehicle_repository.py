import logging
from uuid import UUID

from .base_repository import BaseRepository
from app.database.models.vehicle_model import VehicleModel

logger = logging.getLogger(__name__)


class VehicleRepository(BaseRepository[VehicleModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = VehicleModel

    def activate(self, vehicle_id: UUID):
        return self.update(vehicle_id, {'is_active': True})

    def deactivate(self, vehicle_id: UUID):
        return self.update(vehicle_id, {'is_active': False})
