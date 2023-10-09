from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ..core.enums.role_enum import RoleEnum


class DecodedJWT(BaseModel):
    id: UUID
    role: RoleEnum
    exp: datetime
