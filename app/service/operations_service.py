import logging
import os
from uuid import UUID

from app.core.enums.request_enum import RequestStatusEnum
from app.core.enums.sinister_enum import SinisterStatusEnum
from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.exceptions.repo_exceptions import BaseRepoException
from app.exceptions.repo_exceptions import NotFoundError
from app.repository.request_repository import RequestRepository
from app.repository.sinister_repository import SinisterRepository
from app.repository.vehicle_repository import VehicleRepository
from app.schemas.operations_schemas import OperationsRequestReq
from app.schemas.operations_schemas import OperationsRequestRes
from app.schemas.operations_schemas import OperationsRequestUpdateReq
from app.schemas.operations_schemas import OperationsSinisterReq
from app.schemas.operations_schemas import OperationsSinisterRes
from app.schemas.operations_schemas import OperationsSinisterUpdateReq

logger = logging.getLogger(__name__)


class OperationsService():
    folder_path_sinisters: str = './files/sinisters'
    folder_path_requests: str = './files/requests/tires'

    def __init__(self) -> None:
        self.__request_repo = None
        self.__sinister_repo = None
        self.__vehicle_repo = None

    @property
    def vehicle_repo(self) -> VehicleRepository:
        if self.__vehicle_repo is None:
            self.__vehicle_repo = VehicleRepository()
        return self.__vehicle_repo

    @property
    def request_repo(self) -> RequestRepository:
        if self.__request_repo is None:
            self.__request_repo = RequestRepository()
        return self.__request_repo

    @property
    def sinister_repo(self) -> SinisterRepository:
        if self.__sinister_repo is None:
            self.__sinister_repo = SinisterRepository()
        return self.__sinister_repo

    def get_branch_requests(self, branch_id: UUID, limit: int, offset: int):
        requests = self.request_repo.get_branch_requests(
            branch_id, limit, offset)
        return requests

    def get_request_by_id(self, branch_id: UUID, request_id: UUID) -> OperationsRequestRes:
        try:
            request = self.request_repo.get_branch_request_by_id(
                branch_id, request_id)
            return OperationsRequestRes.from_orm(request)
        except NotFoundError:
            raise ce.NotFound('Request not found in current branch.')

    def add_new_request(self, branch_id: UUID, request_data: OperationsRequestReq) -> OperationsRequestRes:
        try:
            vehicle_id = request_data.vehicle_id
            self.vehicle_repo.get_by_id(vehicle_id, {'branch_id': branch_id})
            new_request = self.request_repo.create({
                **request_data.dict(),
            })
            return new_request
        except NotFoundError:
            raise ce.NotFound('Vehicle not found in current branch.')
        except BaseRepoException as ex:
            raise se.InternalServerError(ex.args)

    def approve_request(self, branch_id: UUID, request_id: UUID, approver_user_id: UUID,
                        status: SinisterStatusEnum = RequestStatusEnum.APPROVED):
        try:
            request = self.request_repo.get_branch_request_by_id(
                branch_id, request_id)
            if request:
                return self.request_repo.update(request_id, {
                    'status': status,
                    'approver_user_id': approver_user_id,
                })
        except NotFoundError:
            raise ce.NotFound('Request not found in current branch.')
        except BaseRepoException as ex:
            raise se.InternalServerError(ex.args)

    def update_request(self, branch_id: UUID, request_id: UUID,
                       request_data: OperationsRequestUpdateReq) -> OperationsRequestRes:
        try:
            request = self.request_repo.get_branch_request_by_id(
                branch_id, request_id)
            if request:
                return self.request_repo.update(request_id, request_data.dict(exclude_none=True))
        except NotFoundError:
            raise ce.NotFound('Request not found in current branch.')
        except BaseRepoException as ex:
            raise se.InternalServerError(ex.args)

    def delete_request(self, branch_id: UUID, request_id: UUID) -> None:
        try:
            request = self.request_repo.get_branch_request_by_id(
                branch_id, request_id)
            if request:
                return self.request_repo.delete(request_id)
        except NotFoundError:
            raise ce.NotFound('Request not found in current branch.')
        except BaseRepoException as ex:
            raise se.InternalServerError(ex.args)

    def upload_request_file(self, branch_id, content_file, file_name, request_id) -> None:
        try:
            request = self.request_repo.get_branch_request_by_id(
                branch_id, request_id)
            if request:
                with open(f'{self.folder_path_requests}/{request_id}_{file_name}', 'wb') as file:
                    file.write(content_file)

                tire_image = file_name
                update_request = {'tire_image': tire_image}

                self.request_repo.update(request_id, update_request)
            return
        except NotFoundError:
            raise ce.NotFound('Request not found in current branch.')
        except Exception as ex:
            raise ex

    def get_request_download_path(self, branch_id: UUID, request_id: UUID, file_name: str) -> str:
        try:
            request = self.request_repo.get_branch_request_by_id(
                branch_id, request_id)
            if request:
                return f'{self.folder_path_requests}/{request_id}_{file_name}'
        except NotFoundError:
            raise ce.NotFound('Request not found in current branch.')
        except Exception as ex:
            raise ex

    def delete_request_file(self, branch_id: UUID, request_id: UUID, file_name: str):
        try:
            file_path = self.get_request_download_path(
                branch_id, request_id, file_name)
            update_request = {'tire_image': ''}
            self.request_repo.update(request_id, update_request)
            try:
                return os.remove(file_path)
            except FileNotFoundError:
                raise ce.NotFound('File not found in request.')
            except Exception as ex:
                raise ex
        except NotFoundError:
            raise ce.NotFound('Request not found in current branch.')
        except Exception as ex:
            raise ex

    def get_branch_sinisters(self, branch_id: UUID, limit: int, offset: int):
        sinisters = self.sinister_repo.get_branch_sinisters(
            branch_id, limit, offset)
        return sinisters

    def get_sinister_by_id(self, branch_id: UUID, sinister_id: UUID) -> OperationsSinisterRes:
        try:
            sinister = self.sinister_repo.get_branch_sinister_by_id(
                branch_id, sinister_id)
            return OperationsSinisterRes.from_orm(sinister)
        except NotFoundError:
            raise ce.NotFound('Sinister not found in current branch.')

    def add_new_sinister(self, branch_id: UUID, sinister_data: OperationsSinisterReq) -> OperationsSinisterRes:
        try:
            vehicle_id = sinister_data.vehicle_id
            self.vehicle_repo.get_by_id(vehicle_id, {'branch_id': branch_id})
            new_sinister = self.sinister_repo.create({
                **sinister_data.dict(),
            })
            return new_sinister
        except NotFoundError:
            raise ce.NotFound('Vehicle not found in current branch.')
        except BaseRepoException as ex:
            raise se.InternalServerError(ex.args)

    def approve_sinister(self, branch_id: UUID, sinister_id: UUID, approver_user_id: UUID,
                         status: SinisterStatusEnum = SinisterStatusEnum.APPROVED):
        try:
            sinister = self.sinister_repo.get_branch_sinister_by_id(
                branch_id, sinister_id)
            if sinister:
                return self.sinister_repo.update(sinister_id, {
                    'status': status,
                    'approver_user_id': approver_user_id
                })
        except NotFoundError:
            raise ce.NotFound('Sinister not found in current branch.')
        except BaseRepoException as ex:
            raise se.InternalServerError(ex.args)

    def update_sinister(self, branch_id: UUID, sinister_id: UUID,
                        sinister_data: OperationsSinisterUpdateReq) -> OperationsSinisterRes:
        try:
            sinister = self.sinister_repo.get_branch_sinister_by_id(
                branch_id, sinister_id)
            if sinister:
                return self.sinister_repo.update(sinister_id, sinister_data.dict(exclude_none=True))
        except NotFoundError:
            raise ce.NotFound('Sinister not found in current branch.')
        except BaseRepoException as ex:
            raise se.InternalServerError(ex.args)

    def delete_sinister(self, branch_id: UUID, sinister_id: UUID) -> None:
        try:
            sinister = self.sinister_repo.get_branch_sinister_by_id(
                branch_id, sinister_id)
            if sinister:
                return self.sinister_repo.delete(sinister_id)
        except NotFoundError:
            raise ce.NotFound('Sinister not found in current branch.')
        except BaseRepoException as ex:
            raise se.InternalServerError(ex.args)

    def upload_sinister_file(self, branch_id, content_file, file_name, sinister_id) -> None:
        try:
            sinister = self.sinister_repo.get_branch_sinister_by_id(
                branch_id, sinister_id)
            if sinister:
                with open(f'{self.folder_path_sinisters}/{sinister_id}_{file_name}', 'wb') as file:
                    file.write(content_file)

                files_urls = set(sinister.files_urls)
                files_urls.add(file_name)
                update_sinister = {'files_urls': list(files_urls)}

                self.sinister_repo.update(sinister_id, update_sinister)
            return
        except NotFoundError:
            raise ce.NotFound('Sinister not found in current branch.')
        except Exception as ex:
            raise ex

    def get_sinister_download_path(self, branch_id: UUID, sinister_id: UUID, file_name: str) -> str:
        try:
            sinister = self.sinister_repo.get_branch_sinister_by_id(
                branch_id, sinister_id)
            if sinister:
                return f'{self.folder_path_sinisters}/{sinister_id}_{file_name}'
        except NotFoundError:
            raise ce.NotFound('Sinister not found in current branch.')
        except Exception as ex:
            raise ex

    def delete_sinister_file(self, branch_id: UUID, sinister_id: UUID, file_name: str):
        try:
            file_path = self.get_sinister_download_path(
                branch_id, sinister_id, file_name)
            sinister = self.sinister_repo.get_by_id(sinister_id)
            files_urls = set(sinister.files_urls)
            files_urls.remove(file_name)
            update_sinister = {'files_urls': list(files_urls)}
            self.sinister_repo.update(sinister_id, update_sinister)
            try:
                return os.remove(file_path)
            except FileNotFoundError:
                raise ce.NotFound('File not found in sinister.')
            except Exception as ex:
                raise ex
        except NotFoundError:
            raise ce.NotFound('Sinister not found in current branch.')
        except Exception as ex:
            raise ex
