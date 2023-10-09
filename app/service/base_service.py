import logging
from typing import Callable
from typing import Generic
from typing import List
from typing import TypeVar
from uuid import UUID

from pydantic import BaseModel as SchemaBase

from ..database.models import BaseModel
from ..repository.base_repository import BaseRepository
from app.exceptions.client_exceptions import BadRequest
from app.exceptions.client_exceptions import NotFound
from app.exceptions.repo_exceptions import DatabaseError
from app.exceptions.repo_exceptions import NotFoundError
from app.exceptions.server_exceptions import InternalServerError


logger = logging.getLogger(__name__)

InputSchemaType = TypeVar('InputSchemaType', bound=SchemaBase)
OutputSchemaType = TypeVar('OutputSchemaType', bound=SchemaBase)
ModelType = TypeVar('ModelType', bound=BaseModel)
RepoType = TypeVar('RepoType', bound=BaseRepository)


class BaseService(Generic[ModelType, InputSchemaType, OutputSchemaType, RepoType]):
    def __init__(self, RepoClass: Callable):
        self.repo: RepoType = RepoClass()

    def create(self, new_resource_schema: SchemaBase) -> OutputSchemaType:
        try:
            new_resource_model = self.repo.create(new_resource_schema.dict())

            return self._to_schema(new_resource_model)
        except DatabaseError as dbe:
            # TODO: logger for the error
            raise BadRequest(dbe.message)
        except Exception as ex:
            logger.critical('Not handled error')
            logger.error(ex.args)
            raise InternalServerError()

    def get_all(self, limit: int = 10, offset: int = 0, search_filter: dict = None) -> List[OutputSchemaType]:
        try:
            resource_list = self.repo.get_all(limit, offset, search_filter)

            return [self._to_schema(model_resource) for model_resource in resource_list]
        except Exception as ex:
            logger.critical('Not handled error')
            logger.error(ex.args)
            raise InternalServerError()

    def get_by_id(self, id: UUID) -> OutputSchemaType:
        try:
            return self._to_schema(self.repo.get_by_id(id))
        except NotFoundError as err:
            raise NotFound('; '.join(err.args))
        except Exception as ex:
            logger.critical('Not handled error')
            logger.error(ex.args)
            raise InternalServerError()

    def update(self, resource_id: UUID, new_data: SchemaBase) -> ModelType:
        try:
            updated_resource = self.repo.update(
                resource_id, new_data.dict(exclude_none=True))
            return self._to_schema(updated_resource, 'update')
        except Exception as ex:
            raise InternalServerError(ex.args)

    def delete(self, id: UUID) -> None:
        try:
            self.repo.delete(id)
            return
        except NotFoundError as err:
            raise NotFound('; '.join(err.args))

    def _to_schema(self, model: ModelType) -> OutputSchemaType:
        raise NotImplementedError(
            'This method must be implemented in subclasses')
