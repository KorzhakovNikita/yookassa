from dataclasses import dataclass
from uuid import UUID

from src.domain.payment.entities.payment import Payment
from src.domain.refund.entities.refund import Refund
from src.domain.shared.value_objects.money import Money


@dataclass
class RefundCreationData:
    refund: Refund
    gateway_refund_id: UUID


@dataclass
class RefundPaymentResult:
    payment: Payment
    refund: Refund
    refunded_amount: Money
    message: str = "Payment refunded successfully"


@dataclass
class RefundWithTechnicalData:
    refund: Refund
    gateway_refund_id: UUID
