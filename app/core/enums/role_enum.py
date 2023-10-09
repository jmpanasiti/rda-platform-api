from enum import Enum


class RoleEnum(str, Enum):
    superadmin = 'superadmin'  # RDA IT
    admin = 'admin'  # Ejecutivo RDA
    manager = 'manager'
    supermanager = 'supermanager'
    agent = 'agent'  # nivel branch
    provider = 'provider'
    driver = 'driver'


ADMIN_ROLES = [RoleEnum.superadmin, RoleEnum.admin]
ALL_ROLES = [
    RoleEnum.superadmin,
    RoleEnum.admin,
    RoleEnum.manager,
    RoleEnum.supermanager,
    RoleEnum.agent,
    RoleEnum.provider,
    RoleEnum.driver,
]
MANAGER_ROLES = [RoleEnum.supermanager, RoleEnum.manager, RoleEnum.agent]


def role_list_to_str(role_list: list) -> str:
    return ', '.join(role_list)
