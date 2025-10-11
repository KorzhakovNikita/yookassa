from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.domain.refund.value_objects.refund_status import RefundStatus
from src.domain.shared.value_objects.money import Money


@dataclass
class Refund:
    id: UUID
    payment_id: UUID
    amount: Money
    status: RefundStatus
    created_at: datetime
    reason: Optional[str] = None
    refunded_at: Optional[datetime] = None

    def mark_as_succeeded(self) -> None:
        self.status = RefundStatus.SUCCEEDED
        self.refunded_at = datetime.utcnow()

