import logging
from typing import Type
from uuid import UUID

from sqlalchemy.exc import NoResultFound

from ..database.models import SinisterModel
from ..database.models import VehicleModel
from .base_repository import BaseRepository
from app.exceptions.repo_exceptions import NotFoundError

logger = logging.getLogger(__name__)
DEFAULT_FILTER = {'is_deleted': False}


class SinisterRepository(BaseRepository[SinisterModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = SinisterModel

    def get_branch_sinisters(self, branch_id: UUID, limit: int, offset: int = 0) -> list[Type[SinisterModel]]:
        try:
            query = self.db.query(self.model).filter(
                self.model.vehicle.has(VehicleModel.branch_id == branch_id))
            return query.offset(offset).limit(limit).all()
        except Exception as ex:
            raise ex

    def get_branch_sinister_by_id(self, branch_id, sinister_id, search_filter: dict = None):
        if search_filter is None:
            search_filter = DEFAULT_FILTER

        query = self.db.query(self.model).filter(self.model.vehicle.has(VehicleModel.branch_id == branch_id))\
            .filter_by(id=sinister_id, **search_filter)
        try:
            return query.one()
        except NoResultFound:
            raise NotFoundError(
                f'No resource was found in "{self.model.__name__}" with the id "{sinister_id}"'
            )
        except Exception as ex:
            raise ex
