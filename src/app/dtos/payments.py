from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID

from src.domain.payment.entities.payment import Payment


@dataclass
class PaymentCreationData:
    payment: Payment
    confirmation_url: Optional[str] = None
    payment_method: Optional[str] = None
    refundable: bool = False
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    idempotency_key: Optional[UUID] = None
    cancelled_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


@dataclass
class CreatePaymentResult:
    payment: Payment
    confirmation_url: str


