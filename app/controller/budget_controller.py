import logging
from typing import List
from uuid import UUID

from fastapi import UploadFile
from fastapi.responses import FileResponse

from app.exceptions import server_exceptions as se
from app.exceptions.base_http_exception import BaseHTTPException
from app.schemas.budget_schemas import BudgetRequest
from app.schemas.budget_schemas import BudgetResponse
from app.service.budget_service import BudgetService

logger = logging.getLogger(__name__)


class BudgetController():
    def __init__(self) -> None:
        self.__budget_service = None

    @property
    def budget_service(self) -> BudgetService:
        if self.__budget_service is None:
            self.__budget_service = BudgetService()
        return self.__budget_service

    def create(self, budget: BudgetRequest) -> BudgetResponse:
        try:
            new_budget = self.budget_service.create(budget)
            return new_budget

        except BaseHTTPException as ex:
            raise ex
        except Exception as ex:
            logger.critical("Not handled error")
            logger.error('; '.join(ex.args))
            raise se.InternalServerError(
                'Something went wrong, contact the admin')

    def get_list_paginated(self, limit: int, offset: int) -> List[BudgetResponse]:
        try:
            budgets_list = self.budget_service.get_all(limit, offset)

            return budgets_list
        except Exception as ex:
            logger.critical(f'Unhandled error: {"; ".join(ex.args)}')
            raise se.InternalServerError(
                'Something went wrong on listing budgets. Please contact the sysadmin')

    def get_by_id(self, budget_id: UUID) -> BudgetResponse:
        try:
            return self.budget_service.get_by_id(budget_id)
        except BaseHTTPException as ex:
            raise ex

    def update(self, budget_id: UUID, budget_data: BudgetRequest) -> BudgetResponse:
        try:
            return self.budget_service.update(budget_id, budget_data)
        except BaseHTTPException as ex:
            raise ex

    def delete(self, budget_id: UUID) -> None:
        try:
            self.budget_service.delete(budget_id)
        except BaseHTTPException as ex:
            raise ex

    async def upload_allocation_file(self, budget_id: UUID, file: UploadFile):
        try:
            content_file = await file.read()
            self.budget_service.upload_allocation_file(
                budget_id, content_file, file.filename)
        except BaseHTTPException as ex:
            raise ex

    def download_budget(self, budget_id: UUID):
        try:
            file_path = self.budget_service.get_download_path(budget_id)
            return FileResponse(file_path)
        except BaseHTTPException as ex:
            raise ex
