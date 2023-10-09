import logging
from uuid import UUID

from sqlalchemy.exc import NoResultFound

from .base_repository import BaseRepository
from app.database.models.user_model import UserModel
from app.exceptions.repo_exceptions import NotFoundError

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository[UserModel]):
    def __init__(self) -> None:
        super().__init__()
        self.model = UserModel

    def get_by_username(self, username: str) -> UserModel:
        query = self.db.query(self.model).filter_by(
            username=username, is_deleted=False)
        try:
            return query.one()
        except NoResultFound:
            logger.warning(f'Not found user "{username}"')
            raise NotFoundError(
                f'No resource was found in "{UserModel.__name__}" with the username "{username}"'
            )

        finally:
            self.db.close()

    def activate(self, user_id: UUID):
        return self.update(user_id, {'is_active': True})

    def deactivate(self, user_id: UUID):
        return self.update(user_id, {'is_active': False})
