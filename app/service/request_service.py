from ..database.models import RequestModel
from ..repository.request_repository import RequestRepository as RequestRepo
from ..schemas.request_schemas import ServiceRequestReq
from ..schemas.request_schemas import ServiceRequestRes
from .base_service import BaseService


class RequestService(BaseService[RequestModel, ServiceRequestReq, ServiceRequestRes, RequestRepo]):

    def __init__(self):
        super().__init__(RequestRepo)

    def _to_schema(self, model: RequestModel | dict, *args) -> ServiceRequestRes:
        if type(model) is dict:
            return ServiceRequestRes(**model)

        return ServiceRequestRes(
            id=model.id,
            type=model.type,
            status=model.status,
            details=model.details,
            odometer=model.odometer,
            appointment_date=model.appointment_date,
            alternative_date=model.alternative_date,
            emergency=model.emergency,
            tire_quantity=model.tire_quantity,
            tire_brand=model.tire_brand,
            tire_alternative_brand=model.tire_alternative_brand,
            tire_measure=model.tire_measure,
            tire_image=model.tire_image,
            tire_reason=model.tire_reason,
            verification_type=model.verification_type,
            user_validation=model.user_validation,
            zone=model.zone,
            vehicle_id=model.vehicle_id,
            vehicle=model.vehicle,
            user_id=model.user_id,
            approver_user_id=model.approver_user_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
