import logging
from typing import List
from uuid import UUID

from app.core.enums.role_enum import RoleEnum as Role
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.exceptions.base_http_exception import BaseHTTPException
from app.schemas.branch_schemas import BranchRequest
from app.schemas.branch_schemas import BranchResponse
from app.schemas.token_schemas import DecodedJWT
from app.service.branch_service import BranchService
from app.service.user_service import UserService

logger = logging.getLogger(__name__)


class BranchController():
    def __init__(self) -> None:
        self.__branch_service = None
        self.__user_service = None

    @property
    def branch_service(self) -> BranchService:
        if self.__branch_service is None:
            self.__branch_service = BranchService()
        return self.__branch_service

    @property
    def user_service(self) -> UserService:
        if self.__user_service is None:
            self.__user_service = UserService()
        return self.__user_service

    def create(self, branch: BranchRequest, token: DecodedJWT) -> BranchResponse:
        try:
            if token.role == Role.supermanager:
                current_user = self.user_service.get_by_id(token.id)
                if current_user.branch.organization_id != branch.organization_id:
                    raise ce.Forbidden(
                        'You can\'t create a branch to this organization')

            new_branch = self.branch_service.create(branch)
            return new_branch

        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.critical("Not handled error")
            logger.error('; '.join(ex.args))
            raise se.InternalServerError(
                'Something went wrong, contact the admin')

    def get_list_paginated(self, limit: int, offset: int, token: DecodedJWT) -> List[BranchResponse]:
        try:
            search_filter = {}
            if token.role == Role.supermanager:
                current_user = self.user_service.get_by_id(token.id)
                search_filter.update(
                    organization_id=current_user.branch.organization_id)
            branche_list = self.branch_service.get_all(
                limit, offset, search_filter)

            return branche_list
        except Exception as ex:
            logger.critical(f'Unhandled error: {"; ".join(ex.args)}')
            raise se.InternalServerError(
                'Something went wrong on listing branches. Please contact the sysadmin')

    def get_by_id(self, branch_id: UUID) -> BranchResponse:
        try:
            return self.branch_service.get_by_id(branch_id)
        except BaseHTTPException as ex:
            raise ex

    def update(self, branch_id: UUID, branch_data: BranchRequest, token: DecodedJWT) -> BranchResponse:
        try:
            if token.role == Role.supermanager:
                current_branch = self.branch_service.get_by_id(branch_id)
                if current_branch.organization.super_manager_id != token.id:
                    raise ce.Forbidden('You can\'t edit this branch')
            return self.branch_service.update(branch_id, branch_data)
        except BaseHTTPException as ex:
            raise ex

    def delete(self, branch_id: UUID) -> None:
        try:
            self.branch_service.delete(branch_id)
        except BaseHTTPException as ex:
            raise ex
