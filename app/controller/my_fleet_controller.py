from typing import List
from uuid import UUID

from app.schemas.my_fleet_schemas import MyFleetUserReq
from app.schemas.my_fleet_schemas import MyFleetUserRes
from app.schemas.my_fleet_schemas import MyFleetUserUpdateReq
from app.schemas.my_fleet_schemas import MyFleetVehicleReq
from app.schemas.my_fleet_schemas import MyFleetVehicleRes
from app.schemas.my_fleet_schemas import MyFleetVehicleUpdateReq
from app.service.my_fleet_service import MyFleetService


class MyFleetController():
    def __init__(self) -> None:
        self.__my_fleet_service = None

    @property
    def my_fleet_service(self) -> MyFleetService:
        if self.__my_fleet_service is None:
            self.__my_fleet_service = MyFleetService()
        return self.__my_fleet_service

    def get_vehicles_paginated(self, limit: int, offset: int, branch_id: UUID) -> List[MyFleetVehicleRes]:
        vehicles = self.my_fleet_service.get_fleet_vehicles(
            limit, offset, branch_id)
        return vehicles

    def get_vehicle_by_id(self, branch_id: UUID, vehicle_id: UUID) -> MyFleetVehicleRes:
        return self.my_fleet_service.get_vehicle_by_id(branch_id, vehicle_id)

    def add_new_vehicle(self, branch_id: UUID, vehicle_data: MyFleetVehicleReq):
        return self.my_fleet_service.add_new_vehicle(vehicle_data, branch_id)

    def update_vehicle(self, branch_id: UUID, vehicle_id: UUID, vehicle_data: MyFleetVehicleUpdateReq) -> MyFleetVehicleRes:
        # TODO: validar que el vehiculo pertenezca al branch
        return self.my_fleet_service.update_vehicle(vehicle_id, vehicle_data)

    def delete_vehicle(self, branch_id: UUID, vehicle_id: UUID) -> None:
        # TODO: validar que el vehiculo pertenezca al branch
        return self.my_fleet_service.delete_vehicle(vehicle_id)

    def activate_vehicle(self, branch_id: UUID, vehicle_id: UUID) -> None:
        # TODO: validar que el vehiculo pertenezca al branch
        return self.my_fleet_service.set_is_active_vehicle(vehicle_id)

    def deactivate_vehicle(self, branch_id: UUID, vehicle_id: UUID) -> None:
        # TODO: validar que el vehiculo pertenezca al branch
        return self.my_fleet_service.set_is_active_vehicle(vehicle_id, is_active=False)

    def get_users_paginated(self, limit: int, offset: int, branch_id: UUID) -> List[MyFleetUserRes]:
        # users = self.user_service.get_all(limit, offset)
        users = self.my_fleet_service.get_fleet_users(limit, offset, branch_id)
        return users

    def get_user_by_id(self, branch_id: UUID, user_id: UUID) -> MyFleetUserRes:
        return self.my_fleet_service.get_user_by_id(branch_id, user_id)

    def add_new_user(self, branch_id: UUID, user_data: MyFleetUserReq):
        return self.my_fleet_service.add_new_user(user_data, branch_id)

    def update_user(self, branch_id: UUID, user_id: UUID, user_data: MyFleetUserUpdateReq) -> MyFleetUserRes:
        # TODO: validar que el vehiculo pertenezca al branch
        return self.my_fleet_service.update_user(user_id, user_data)

    def delete_user(self, branch_id: UUID, user_id: UUID) -> None:
        # TODO: validar que el vehiculo pertenezca al branch
        return self.my_fleet_service.delete_user(user_id)

    def activate_user(self, branch_id: UUID, user_id: UUID) -> None:
        # TODO: validar que el vehiculo pertenezca al branch
        return self.my_fleet_service.set_is_active_user(user_id)

    def deactivate_user(self, branch_id: UUID, user_id: UUID) -> None:
        # TODO: validar que el vehiculo pertenezca al branch
        return self.my_fleet_service.set_is_active_user(user_id, is_active=False)
