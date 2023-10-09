import logging
from typing import List
from uuid import UUID

from app.exceptions import client_exceptions as ce
from app.exceptions import server_exceptions as se
from app.exceptions.repo_exceptions import BaseRepoException
from app.exceptions.repo_exceptions import NotFoundError
from app.repository.user_repository import UserRepository
from app.repository.vehicle_repository import VehicleRepository
from app.schemas.my_fleet_schemas import MyFleetUserReq
from app.schemas.my_fleet_schemas import MyFleetUserRes
from app.schemas.my_fleet_schemas import MyFleetUserUpdateReq
from app.schemas.my_fleet_schemas import MyFleetVehicleReq
from app.schemas.my_fleet_schemas import MyFleetVehicleRes
from app.schemas.my_fleet_schemas import MyFleetVehicleUpdateReq

logger = logging.getLogger(__name__)


class MyFleetService():
    def __init__(self) -> None:
        self.__vehicle_repo = None
        self.__user_repo = None

    @property
    def vehicle_repo(self) -> VehicleRepository:
        if self.__vehicle_repo is None:
            self.__vehicle_repo = VehicleRepository()
        return self.__vehicle_repo

    @property
    def user_repo(self) -> UserRepository:
        if self.__user_repo is None:
            self.__user_repo = UserRepository()
        return self.__user_repo

    def get_fleet_vehicles(self, limit: int, offset: int, branch_id: UUID) -> List[MyFleetVehicleRes]:
        vehicles = self.vehicle_repo.get_all(
            limit, offset, search_filter={'branch_id': branch_id})
        return vehicles

    def get_vehicle_by_id(self, branch_id: UUID, vehicle_id: UUID) -> MyFleetVehicleRes:
        try:
            vehicle = self.vehicle_repo.get_by_id(
                vehicle_id, {'branch_id': branch_id})

            return MyFleetVehicleRes.from_orm(vehicle)
        except NotFoundError:
            raise ce.NotFound('Vehicle not found in current branch.')

    def add_new_vehicle(self, vehicle_data: MyFleetVehicleReq, branch_id: UUID) -> MyFleetVehicleRes:
        try:
            new_vehicle = self.vehicle_repo.create({
                **vehicle_data.dict(),
                'branch_id': branch_id
            })
            return new_vehicle
        except BaseRepoException as ex:
            raise se.InternalServerError(ex.args)

    def update_vehicle(self, vehicle_id: UUID, vehicle_data: MyFleetVehicleUpdateReq) -> MyFleetVehicleRes:
        try:
            return self.vehicle_repo.update(vehicle_id, vehicle_data.dict(exclude_none=True))
        except BaseRepoException as ex:
            raise se.InternalServerError(ex.args)

    def delete_vehicle(self, vehicle_id: UUID) -> None:
        try:
            return self.vehicle_repo.delete(vehicle_id)
        except BaseRepoException as ex:
            raise se.InternalServerError(ex.args)

    def set_is_active_vehicle(self, vehicle_id: UUID, is_active: bool = True) -> None:
        try:
            return self.vehicle_repo.update(vehicle_id, {
                'is_active': is_active,
            })
        except BaseRepoException as ex:
            raise se.InternalServerError(ex.args)

    def get_fleet_users(self, limit: int, offset: int, branch_id: UUID) -> List[MyFleetUserRes]:
        users = self.user_repo.get_all(limit, offset, search_filter={
                                       'branch_id': branch_id})
        return users

    def get_user_by_id(self, branch_id: UUID, user_id: UUID) -> MyFleetUserRes:
        try:
            user = self.user_repo.get_by_id(user_id, {'branch_id': branch_id})

            return MyFleetUserRes.from_orm(user)
        except NotFoundError:
            raise ce.NotFound('User not found in current branch.')

    def add_new_user(self, user_data: MyFleetUserReq, branch_id: UUID) -> MyFleetUserRes:
        try:
            new_user = self.user_repo.create({
                **user_data.dict(),
                'branch_id': branch_id
            })
            return new_user
        except BaseRepoException as ex:
            raise se.InternalServerError(ex.args)

    def update_user(self, user_id: UUID, user_data: MyFleetUserUpdateReq) -> MyFleetUserRes:
        try:
            return self.user_repo.update(user_id, user_data.dict(exclude_none=True))
        except BaseRepoException as ex:
            raise se.InternalServerError(ex.args)

    def delete_user(self, user_id: UUID) -> None:
        try:
            return self.user_repo.delete(user_id)
        except BaseRepoException as ex:
            raise se.InternalServerError(ex.args)

    def set_is_active_user(self, user_id: UUID, is_active: bool = True) -> None:
        try:
            return self.user_repo.update(user_id, {
                'is_active': is_active,
            })
        except BaseRepoException as ex:
            raise se.InternalServerError(ex.args)
