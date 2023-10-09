import logging
from typing import Generic
from typing import List
from typing import TypeVar
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from ..database import rda_db
from ..database.models import BaseModel
from app.exceptions.repo_exceptions import DatabaseError
from app.exceptions.repo_exceptions import NotFoundError

ModelType = TypeVar('ModelType', bound=BaseModel)
logger = logging.getLogger(__name__)
DEFAULT_FILTER = {'is_deleted': False}


class BaseRepository(Generic[ModelType]):
    def __init__(self, db: Session = rda_db.session) -> None:
        self.db = db
        self.model = ModelType

    def create(self, new_resource_dict: dict) -> ModelType:
        try:
            new_resource = self.model()
            for field in new_resource_dict.keys():
                setattr(new_resource, field, new_resource_dict[field])

            self.db.add(new_resource)
            self.db.commit()
            self.db.refresh(new_resource)

            return new_resource
        except IntegrityError as ie:
            self.db.rollback()
            raise DatabaseError('; '.join(ie.args))

    def get_all(self, limit: int = 10, offset: int = 0, search_filter: dict = None) -> List[ModelType]:
        if search_filter is None:
            search_filter = DEFAULT_FILTER
        else:
            search_filter.update(DEFAULT_FILTER)

        try:
            return self.db.query(self.model).filter_by(**search_filter).offset(offset).limit(limit).all()
        except Exception as ex:
            raise ex

    def get_by_id(self, id: UUID, search_filter: dict = None) -> ModelType:
        if search_filter is None:
            search_filter = DEFAULT_FILTER

        query = self.db.query(self.model).filter_by(id=id, **search_filter)
        try:
            return query.one()
        except NoResultFound:
            # TODO: logger
            raise NotFoundError(
                f'No resource was found in "{self.model.__name__}" with the id "{id}"'
            )
        except Exception as ex:
            # TODO: logger
            raise ex

    def get_list_by_filter(self, search_filter: dict) -> List[ModelType]:
        query = self.db.query(self.model).filter_by(**search_filter)
        try:
            return query.all()
        except Exception as ex:
            raise ex

    def update(self, resource_id: UUID, new_data: dict, search_filter: dict = {}) -> ModelType:
        search_filter = dict(**DEFAULT_FILTER, **search_filter)
        try:
            # Get the resource to update
            resource_db = self.get_by_id(resource_id, search_filter)
            # Update the fields that change (dict)
            for field in new_data.keys():
                setattr(resource_db, field, new_data[field])
            # Commit changes
            self.db.commit()
            return resource_db
        except NoResultFound:
            # TODO: logger
            raise NotFoundError(
                f'No resource was found in "{self.model.__name__}" with the id "{id}"'
            )
        except IntegrityError as err:
            logger.error(err.args)
            logger.error(f'Data with error: {str(new_data)}')
            self.db.rollback()
            raise err
        except Exception as ex:
            logger.critical(ex.args)
            self.db.rollback()
            raise ex

    def delete(self, resource_id: UUID) -> None:
        try:
            self.update(resource_id, {'is_deleted': True})
        except Exception as ex:
            # TODO: logger critical
            raise ex
