from dataclasses import dataclass
from uuid import UUID

from src.domain.payment.entities.payment import Payment
from src.domain.refund.entities.refund import Refund


@dataclass
class RefundCreationData:
    refund: Refund
    gateway_refund_id: UUID


@dataclass
class RefundPaymentResult:
    payment: Payment
    refund: Refund
    message: str = "Payment refunded successfully"


@dataclass
class RefundWithTechnicalData:
    refund: Refund
    gateway_refund_id: UUID
