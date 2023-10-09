import logging

from ..core.jwt import jwt_manager
from ..repository.branch_repository import BranchRepository
from ..repository.organization_repository import OrganizationRepository
from ..repository.user_repository import NotFoundError
from ..repository.user_repository import UserRepository
from ..schemas.auth_schemas import LoginSchema
from ..schemas.auth_schemas import RegisterSchema
from app.core.enums.role_enum import RoleEnum as Role
from app.exceptions.client_exceptions import BadRequest
from app.exceptions.client_exceptions import Unauthorized
from app.exceptions.server_exceptions import InternalServerError

logger = logging.getLogger(__name__)


class AuthService():
    def __init__(self) -> None:
        self.user_repo = UserRepository()
        self.org_repo = OrganizationRepository()
        self.branch_repo = BranchRepository()

    def register(self, register_data: RegisterSchema) -> str:
        try:
            # Check if username and email are available
            user_by_username = self.user_repo.get_list_by_filter(
                {'username': register_data.username})
            user_by_email = self.user_repo.get_list_by_filter(
                {'email': register_data.email})
            if (len(user_by_username) > 0):
                raise BadRequest(
                    f'User with username "{register_data.username}" already exists.')
            if (len(user_by_email) > 0):
                raise BadRequest(
                    f'User with email "{register_data.email}" already exists.')

            # Create new user
            new_user = self.user_repo.create({
                'username': register_data.username,
                'email': register_data.email,
                'password': register_data.password,
                'first_name': register_data.first_name,
                'last_name': register_data.last_name,
                'role': Role.supermanager,
            })
            logger.info(
                f'New user {new_user.username} registered successfully.')

            # Create new Organization
            new_org = self.org_repo.create({
                'name': register_data.organization_name,
                'business_name': register_data.organization_name,
                'super_manager_id': new_user.id,
                'contact_id': new_user.id,
            })
            logger.info(f'New org {new_org.name} created successfully.')

            # Create new branch
            new_branch = self.branch_repo.create({
                'name': register_data.branch_name,
                'cost_center': '',
                'area': '',
                'manager_id': new_user.id,
                'organization_id': new_org.id,
            })
            logger.info(f'New branch {new_branch.name} created successfully.')

            # Update user with branch id
            self.user_repo.update(
                new_user.id,
                {'branch_id': new_branch.id},
            )

            # Get token
            payload = {
                'id': str(new_user.id),
                'role': new_user.role,
            }
            return jwt_manager.encode(payload)
        except BadRequest as ex:
            logger.warn(ex.description)
            raise ex
        except Exception as ex:
            logger.error(type(ex))
            logger.critical('Not handled error')
            logger.error(ex.args)
            raise InternalServerError()

    def login(self, credentials: LoginSchema) -> str:
        try:
            user = self.user_repo.get_by_username(credentials.username)
            if not user.check_password(credentials.password):
                raise Unauthorized('Error on username/password')
            payload = {
                'id': str(user.id),
                'role': user.role,
            }
            token = jwt_manager.encode(payload)

            logger.info(f'User {user.username} logged in successfully.')
            return token
        except NotFoundError:
            logger.warn(f'User "{credentials.username}" not found')
            raise Unauthorized('Error on username/password')
        except Unauthorized as err:
            logger.warn(
                f'User {user.username} try to loggin with a wrong password.')
            raise err
        except Exception as ex:
            logger.error(type(ex))
            logger.critical('Not handled error')
            logger.error(ex.args)
            raise InternalServerError()
