from enum import Enum


class BudgetStatusEnum(str, Enum):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
    CANCELLED = 'Cancelled'
