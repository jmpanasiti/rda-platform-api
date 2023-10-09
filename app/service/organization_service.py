from ..database.models import OrganizationModel
from ..repository.organization_repository import OrganizationRepository as OrganizationRepo
from ..schemas.organization_schemas import OrganizationRequest
from ..schemas.organization_schemas import OrganizationResponse
from .base_service import BaseService


class OrganizationService(BaseService[OrganizationModel, OrganizationRequest, OrganizationResponse, OrganizationRepo]):

    def __init__(self):
        super().__init__(OrganizationRepo)

    def _to_schema(self, model: OrganizationModel, *args) -> OrganizationResponse:
        return OrganizationResponse(
            id=model.id,
            name=model.name,
            business_name=model.business_name,
            contact_id=model.contact_id,
            super_manager_id=model.super_manager_id,
            manager_id=model.manager_id,
            document_number=model.document_number,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
