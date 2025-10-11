from enum import Enum


class RefundStatus(str, Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    CANCELLED = "cancelled"
