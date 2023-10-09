from typing import List
from uuid import UUID

from app.core.enums.role_enum import MANAGER_ROLES
from app.core.enums.role_enum import RoleEnum
from app.schemas.my_report_schemas import MyReportSchema
from app.schemas.my_report_schemas import MyReportUserRes
from app.schemas.my_report_schemas import MyReportVehicleRes
from app.service.branch_service import BranchService
from app.service.my_report_service import MyReportService
from app.service.user_service import UserService


class MyReportController():
    def __init__(self) -> None:
        self.__my_report_service = None
        self.__user_service = None
        self.__branch_service = None

    @property
    def my_report_service(self) -> MyReportService:
        if self.__my_report_service is None:
            self.__my_report_service = MyReportService()
        return self.__my_report_service

    @property
    def user_service(self) -> UserService:
        if self.__user_service is None:
            self.__user_service = UserService()
        return self.__user_service

    @property
    def branch_service(self) -> BranchService:
        if self.__branch_service is None:
            self.__branch_service = BranchService()
        return self.branch_service

    def has_permission(self, user_id: UUID, role: RoleEnum, branch_id: UUID) -> bool:

        if role in MANAGER_ROLES:
            user = self.user_service.get_by_id(user_id)
            branch = self.branch_service.get_by_id(branch_id)

            if role == RoleEnum.supermanager:
                if user.branch.organization_id != branch.organization_id:
                    raise PermissionError(
                        'You do not have permissions to access the branch')

            if role == RoleEnum.manager:
                if user.branch_id != branch.id:
                    raise PermissionError(
                        'You do not have permissions to access the branch')

            return True
        return True

    def get_active_vehicles(self) -> List[MyReportSchema]:
        active_vehicles = self.my_report_service.get_active_vehicles()
        return active_vehicles

    def get_vehicles_with_expenses(self, branch_id: UUID, vehicle_id: UUID) -> List[MyReportVehicleRes]:
        vehicles_with_expenses = self.my_report_service.get_vehicles_with_expenses(
            branch_id, vehicle_id)
        return vehicles_with_expenses

    def get_users_with_expenses(self, branch_id: UUID, vehicle_id: UUID) -> List[MyReportUserRes]:
        users_with_expenses = self.my_report_service.get_users_with_expenses(
            branch_id, vehicle_id)
        return users_with_expenses
