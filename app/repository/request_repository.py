import logging
from typing import Type
from uuid import UUID

from sqlalchemy.exc import NoResultFound

from ..database.models import RequestModel
from ..database.models import VehicleModel
from .base_repository import BaseRepository
from app.exceptions.repo_exceptions import NotFoundError


logger = logging.getLogger(__name__)
DEFAULT_FILTER = {'is_deleted': False}


class RequestRepository(BaseRepository[RequestModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = RequestModel

    def get_branch_requests(self, branch_id: UUID, limit: int, offset: int = 0) -> list[Type[RequestModel]]:
        try:
            query = self.db.query(self.model).filter(
                self.model.vehicle.has(VehicleModel.branch_id == branch_id))
            return query.offset(offset).limit(limit).all()
        except Exception as ex:
            raise ex

    def get_branch_request_by_id(self, branch_id, request_id, search_filter: dict = None):
        if search_filter is None:
            search_filter = DEFAULT_FILTER

        query = self.db.query(self.model).filter(self.model.vehicle.has(VehicleModel.branch_id == branch_id))\
            .filter_by(id=request_id, **search_filter)
        try:
            return query.one()
        except NoResultFound:
            raise NotFoundError(
                f'No resource was found in "{self.model.__name__}" with the id "{request_id}"'
            )
        except Exception as ex:
            raise ex
