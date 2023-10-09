from ..database.models import BranchModel
from ..repository.branch_repository import BranchRepository as BranchRepo
from ..schemas.branch_schemas import BranchRequest
from ..schemas.branch_schemas import BranchResponse
from .base_service import BaseService


class BranchService(BaseService[BranchModel, BranchRequest, BranchResponse, BranchRepo]):

    def __init__(self):
        super().__init__(BranchRepo)

    def _to_schema(self, model: BranchModel | dict, *args) -> BranchResponse:
        if type(model) is dict:
            return BranchResponse(**model)

        return BranchResponse(
            id=model.id,
            name=model.name,
            cost_center=model.cost_center,
            area=model.area,
            purchase_order_sent_date=model.purchase_order_sent_date,
            organization_id=model.organization_id,
            organization=model.organization,
            agent_id=model.agent_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
