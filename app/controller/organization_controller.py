import logging
from typing import List
from uuid import UUID

from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.schemas.organization_schemas import OrganizationRequest
from app.schemas.organization_schemas import OrganizationResponse
from app.service.branch_service import BranchService
from app.service.organization_service import OrganizationService

logger = logging.getLogger(__name__)


class OrganizationController():
    def __init__(self) -> None:
        self.__organization_service = None
        self.__branch_service = None

    @property
    def organization_service(self) -> OrganizationService:
        if self.__organization_service is None:
            self.__organization_service = OrganizationService()
        return self.__organization_service

    @property
    def branch_service(self) -> BranchService:
        if self.__branch_service is None:
            self.__branch_service = BranchService()
        return self.__branch_service

    def create(self, organization: OrganizationRequest) -> OrganizationResponse:
        try:
            new_organization = self.organization_service.create(organization)
            return new_organization
        except ce.BadRequest as ex:
            raise ex
        except Exception as ex:
            logger.critical("Not handled error")
            logger.error('; '.join(ex.args))
            raise se.InternalServerError(
                'Something went wrong, contact the admin')

    def get_list_paginated(self, limit: int, offset: int) -> List[OrganizationResponse]:
        try:
            response = self.organization_service.get_all(limit, offset)
            return response
        except Exception as ex:
            logger.critical(f'Unhandled error: {"; ".join(ex.args)}')
            raise se.InternalServerError(
                'Something went wrong on listing orgs. Please contact the sysadmin')

    def get_by_id(self, org_id: UUID):
        try:
            response = self.organization_service.get_by_id(org_id)
            return response
        except ce.NotFound as ex:
            raise ex

    def update(self, org_id: UUID, org_data: OrganizationRequest) -> OrganizationResponse:
        try:
            response = self.organization_service.update(org_id, org_data)
            return response
        except ce.NotFound as ex:
            raise ex

    def delete(self, org_id: UUID):
        try:
            self.organization_service.delete(org_id)
        except ce.NotFound as ex:
            raise ex

    def get_org_branches(self, org_id):
        try:
            response = self.branch_service.get_all(
                search_filter={'organization_id': org_id})
            return response
        except Exception as ex:
            logger.critical(f'Unhandled error: {"; ".join(ex.args)}')
            raise se.InternalServerError(
                'Something went wrong on listing branches. Please contact the sysadmin'
            )
