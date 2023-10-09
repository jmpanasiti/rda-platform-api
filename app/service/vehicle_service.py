import os
from uuid import UUID

from ..database.models import VehicleModel
from ..repository.vehicle_repository import VehicleRepository as VehicleRepo
from ..schemas.vehicle_schemas import VehicleRequest as VehicleReq
from ..schemas.vehicle_schemas import VehicleResponse as VehicleRes
from .base_service import BaseService


class VehicleService(BaseService[VehicleModel, VehicleReq, VehicleRes, VehicleRepo]):
    folder_path_policies: str = './files/vehicles/policies'
    folder_path_idcards: str = './files/vehicles/id_cards'

    def __init__(self):
        super().__init__(VehicleRepo)

    def _to_schema(self, model: VehicleModel | dict, method: str = '') -> VehicleRes:
        if type(model) is dict:
            return VehicleRes(**model)
        return VehicleRes(
            id=model.id,
            registration_plate=model.registration_plate,
            brand=model.brand,
            model=model.model,
            year=model.year,
            fire_extinguisher_expiration_date=model.fire_extinguisher_expiration_date,
            vtv_expiration_date=model.vtv_expiration_date,
            documents_expiration_date=model.documents_expiration_date,
            next_service_date=model.next_service_date,
            policy_number=model.policy_number,
            # scoring_3s=model.scoring_3s,
            engraved_parts=model.engraved_parts,
            policy_file=model.policy_file,
            id_card_file=model.id_card_file,
            fee=model.fee,
            chassis=model.chassis,
            branch_id=model.branch_id,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def activate(self, vehicle_id: UUID) -> VehicleRes:
        return self._to_schema(self.repo.activate(vehicle_id))

    def deactivate(self, vehicle_id: UUID) -> VehicleRes:
        return self._to_schema(self.repo.deactivate(vehicle_id))

    def upload_policy(self, content_file, file_name, vehicle_id) -> None:
        try:
            with open(f'{self.folder_path_policies}/{vehicle_id}_{file_name}', 'wb') as file:
                file.write(content_file)

            policy_file = file_name
            update_vehicle = {'policy_file': policy_file}

            self.repo.update(vehicle_id, update_vehicle)
            return
        except Exception as ex:
            raise ex

    def upload_idcard(self, content_file, file_name, vehicle_id) -> None:
        try:
            with open(f'{self.folder_path_idcards}/{vehicle_id}_{file_name}', 'wb') as file:
                file.write(content_file)

            id_card_file = file_name
            update_vehicle = {'id_card_file': id_card_file}

            self.repo.update(vehicle_id, update_vehicle)
            return
        except Exception as ex:
            raise ex

    def get_download_path_policy(self, vehicle_id: UUID, file_name: str) -> str:
        return f'{self.folder_path_policies}/{vehicle_id}_{file_name}'

    def get_download_path_idcard(self, vehicle_id: UUID, file_name: str) -> str:
        return f'{self.folder_path_idcards}/{vehicle_id}_{file_name}'

    def delete_policy(self, vehicle_id: UUID, file_name: str):
        file_path = self.get_download_path_policy(vehicle_id, file_name)
        update_vehicle = {'policy_file': ''}
        self.repo.update(vehicle_id, update_vehicle)
        return os.remove(file_path)

    def delete_idcard(self, vehicle_id: UUID, file_name: str):
        file_path = self.get_download_path_idcard(vehicle_id, file_name)
        update_vehicle = {'id_card_file': ''}
        self.repo.update(vehicle_id, update_vehicle)
        return os.remove(file_path)
