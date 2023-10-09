import os

from click import UUID

from ..database.models import BudgetModel
from ..repository.budget_repository import BudgetRepository as BudgetRepo
from ..schemas.budget_schemas import BudgetRequest
from ..schemas.budget_schemas import BudgetResponse
from .base_service import BaseService


class BudgetService(BaseService[BudgetModel, BudgetRequest, BudgetResponse, BudgetRepo]):
    allocation_folder_path: str = './files/budgets/allocation_files/'

    def __init__(self):
        super().__init__(BudgetRepo)

    def upload_allocation_file(self, budget_id, content_file, file_name):
        budget = self.repo.get_by_id(budget_id)
        # Delete old file
        if budget.allocation_file != "" and os.path.exists(self.allocation_folder_path + budget.allocation_file):
            os.remove(self.allocation_folder_path + budget.allocation_file)
        # Create new one
        with open(f'{self.allocation_folder_path}/{budget.id}_{file_name}', 'wb') as file:
            file.write(content_file)
        self.repo.update(
            budget_id, {"allocation_file": f"{budget.id}_{file_name}"})

    def get_download_path(self, budget_id: UUID) -> str:
        budget = self.repo.get_by_id(budget_id)
        return f'{self.allocation_folder_path}/{budget.allocation_file}'

    def _to_schema(self, model: BudgetModel | dict, *args) -> BudgetResponse:
        # breakpoint()
        if type(model) is dict:
            return BudgetResponse(**model)

        return BudgetResponse(
            id=model.id,
            user_id=model.user_id,
            amount=float(model.amount),
            work_order=model.work_order_id,
            vehicle_id=model.vehicle_id,
            detail=model.detail,
            approval_date=model.approval_date,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
