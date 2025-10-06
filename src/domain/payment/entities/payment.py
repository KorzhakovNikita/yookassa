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
    cancelled_at: Optional[datetime] = None

    def can_be_captured(self) -> bool:
        return self.status == PaymentStatus.WAITING_FOR_CAPTURE

    def can_be_cancelled(self) -> bool:
        return self.status == PaymentStatus.WAITING_FOR_CAPTURE

    def is_active(self) -> bool:
        valid_statuses = (PaymentStatus.PENDING, PaymentStatus.WAITING_FOR_CAPTURE)
        return self.status in valid_statuses and not self.is_expired()

    def is_expired(self) -> bool:
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at

    def mark_as_succeeded(self, capture_date: datetime) -> None:
        if self.status != PaymentStatus.WAITING_FOR_CAPTURE:
            raise InvalidPaymentStatusError(
                f"Only waiting_for_capture payments can be succeeded. Current status: {self.status}"
            )
        self.status = PaymentStatus.SUCCEEDED
        self.captured_at = capture_date

    def mark_as_cancelled(self) -> None:
        self.status = PaymentStatus.CANCELED
        self.cancelled_at = datetime.utcnow()

