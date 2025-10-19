from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID

from src.domain.payment.entities.payment import Payment
from src.infrastucture.database.models import PaymentORM


@dataclass
class PaymentCreationData:
    payment: Payment
    gateway_payment_id: str
    confirmation_url: Optional[str] = None
    payment_method: Optional[str] = None
    refundable: bool = False
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    idempotency_key: Optional[UUID] = None
    cancelled_at: Optional[datetime] = None


@dataclass
class CreatePaymentResult:
    payment: Payment
    confirmation_url: str


@dataclass
class PaymentTechnicalDataUpdate:
    payment_method: Optional[str] = None
    refundable: Optional[bool] = None
    confirmation_url: Optional[str] = None

    def apply_to_orm(self, orm_payment: PaymentORM) -> None:
        for field_name, value in asdict(self).items():
            if value is not None:
                setattr(orm_payment, field_name, value)


@dataclass
class PaymentWithTechnicalData:
    payment: Payment
    gateway_payment_id: Optional[str] = None
    confirmation_url: Optional[str] = None
    payment_method: Optional[str] = None
    idempotency_key: Optional[str] = None


@dataclass
class CancelPaymentResult:
    payment: Payment
    cancelled_at: datetime
    message: str = "Payment cancelled successfully"


@dataclass
class CapturePaymentResult:
    payment: Payment
    captured_at: datetime
    message: str = "Payment captured successfully"
