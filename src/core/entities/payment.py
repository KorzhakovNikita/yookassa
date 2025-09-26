from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.core.exceptions.payment_error import InvalidPaymentStatusError
from src.core.interfaces.models import AbstractModel
from src.core.value_objects.payment_status import PaymentStatus


@dataclass
class Payment(AbstractModel):

    id: UUID
    amount: float
    currency: str
    status: PaymentStatus
    user_id: UUID
    order_id: UUID
    created_at: datetime
    captured_at: Optional[datetime] = None

    def can_be_captured(self) -> bool:
        return self.status == PaymentStatus.WAITING_FOR_CAPTURE

    def can_be_cancelled(self) -> bool:
        return self.status in (PaymentStatus.PENDING, PaymentStatus.WAITING_FOR_CAPTURE)

    def mark_as_succeeded(self, capture_date: datetime) -> None:
        if self.status != PaymentStatus.WAITING_FOR_CAPTURE:
            raise InvalidPaymentStatusError(
                f"Only waiting_for_capture payments can be succeeded. Current status: {self.status}"
            )
        self.status = PaymentStatus.SUCCEEDED
        self.captured_at = capture_date

    def mark_as_cancelled(self) -> None:
        if not self.can_be_cancelled():
            raise InvalidPaymentStatusError(
                f"Payment cannot be cancelled in current state: {self.status}"
            )
        self.status = PaymentStatus.CANCELED
