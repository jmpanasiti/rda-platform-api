import os
from uuid import UUID

from ..database.models import SinisterModel
from ..repository.sinister_repository import SinisterRepository as SinisterRepo
from ..schemas.sinister_schemas import SinisterRequest
from ..schemas.sinister_schemas import SinisterResponse
from .base_service import BaseService


class SinisterService(BaseService[SinisterModel, SinisterRequest, SinisterResponse, SinisterRepo]):
    folder_path: str = './files/sinisters'

    def __init__(self):
        super().__init__(SinisterRepo)

    def _to_schema(self, model: SinisterModel, *args) -> SinisterResponse:
        if type(model) is dict:
            return SinisterResponse(**model)

        return SinisterResponse(
            id=model.id,
            details_damage=model.details_damage,
            details_event=model.details_event,
            type=model.type,
            place=model.place,
            zone=model.zone,
            status=model.status,
            files_urls=model.files_urls,
            vehicle_id=model.vehicle_id,
            user_id=model.user_id,
            approver_user_id=model.approver_user_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def upload(self, content_file, file_name, sinister_id) -> None:
        try:
            sinister = self.get_by_id(sinister_id)

            with open(f'{self.folder_path}/{sinister_id}_{file_name}', 'wb') as file:
                file.write(content_file)

            files_urls = set(sinister.files_urls)
            files_urls.add(file_name)
            update_sinister = {'files_urls': list(files_urls)}

            self.repo.update(sinister_id, update_sinister)
            return
        except Exception as ex:
            raise ex

    def get_download_path(self, sinister_id: UUID, file_name: str) -> str:
        return f'{self.folder_path}/{sinister_id}_{file_name}'

    def delete_file(self, sinister_id: UUID, file_name: str):
        sinister = self.get_by_id(sinister_id)
        file_path = self.get_download_path(sinister_id, file_name)
        files_urls = sinister.files_urls
        try:
            files_urls.remove(file_name)
        except Exception:
            pass
        update_sinister = {'files_urls': list(files_urls)}
        self.repo.update(sinister_id, update_sinister)
        return os.remove(file_path)
