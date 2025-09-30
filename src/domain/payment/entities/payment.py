from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.domain.payment.exceptions import InvalidPaymentStatusError
from src.domain.shared.entities.base import Entity
from src.domain.payment.value_objects.payment_status import PaymentStatus
from src.domain.shared.value_objects.money import Money


@dataclass
class Payment(Entity):
    id: UUID
    amount: Money
    status: PaymentStatus
    order_id: UUID
    created_at: datetime
    captured_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    def can_be_captured(self) -> bool:
        return self.status == PaymentStatus.WAITING_FOR_CAPTURE

    def is_active(self) -> bool:
        valid_statuses = (PaymentStatus.PENDING, PaymentStatus.WAITING_FOR_CAPTURE)
        return self.status in valid_statuses and self.expires_at > datetime.utcnow()

    def mark_as_succeeded(self, capture_date: datetime) -> None:
        if self.status != PaymentStatus.WAITING_FOR_CAPTURE:
            raise InvalidPaymentStatusError(
                f"Only waiting_for_capture payments can be succeeded. Current status: {self.status}"
            )
        self.status = PaymentStatus.SUCCEEDED
        self.captured_at = capture_date

    def mark_as_cancelled(self) -> None:
        if not self.is_active():
            raise InvalidPaymentStatusError(
                f"Payment cannot be cancelled in current state: {self.status}"
            )
        self.status = PaymentStatus.CANCELED
