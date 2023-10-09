from typing import List
from uuid import UUID

from app.repository.sinister_repository import SinisterRepository
from app.repository.user_repository import UserRepository
from app.repository.vehicle_repository import VehicleRepository
from app.schemas.my_report_schemas import MyReportSchema
from app.schemas.my_report_schemas import MyReportUserRes
from app.schemas.my_report_schemas import MyReportVehicleRes


class MyReportService():
    def __init__(self) -> None:
        self.__vehicle_repo = None
        self.__user_repo = None
        self.__sinister_repo = None

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

    @property
    def sinister_repo(self) -> SinisterRepository:
        if self.__sinister_repo is None:
            self.__sinister_repo = SinisterRepository()
        return self.__sinister_repo

    def get_active_vehicles(self, limit: int, offset: int, branch_id: UUID) -> List[MyReportSchema]:
        active_vehicles = self.vehicle_repo.get_all(
            limit, offset, search_filter={'branch_id': branch_id, 'is_active': True, })
        return active_vehicles

    def get_vehicles_with_expenses(self, limit: int, offset: int, branch_id: UUID, fee: float) -> List[MyReportVehicleRes]:
        vehicles_with_expenses = self.vehicle_repo.get_all(
            limit, offset, search_filter={'branch_id': branch_id, 'is_active': True, 'fee': fee, })
        return vehicles_with_expenses

    def get_users_with_expenses(self, limit: int, offset: int, branch_id: UUID) -> List[MyReportUserRes]:
        active_users = self.user_repo.get_all(
            limit, offset, search_filter={'branch_id': branch_id, 'is_active': True})

        users_with_expenses = []

        for user in active_users:
            if user.vehicle_id:

                user_vehicle = self.vehicle_repo.get_by_id(user.vehicle_id)

                if user_vehicle.fee:
                    users_with_expenses.append(user)

        return users_with_expenses
