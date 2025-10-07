from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field

from src.app.dtos.payments import CreatePaymentResult, CancelPaymentResult, CapturePaymentResult, \
    PaymentWithTechnicalData


class MoneySchema(BaseModel):
    value: float = Field(..., gt=0)
    currency: str = Field(default="RUB")


class PaymentCreateRequest(BaseModel):
    order_id: UUID
    amount: MoneySchema
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    return_url: Optional[str] = None


class PaymentCreateResponse(BaseModel):
    payment_id: UUID
    order_id: UUID
    amount: MoneySchema
    status: str
    created_at: datetime
    confirmation_url: str
    expires_at: Optional[datetime] = None

    @classmethod
    def from_result(cls, result: CreatePaymentResult):
        return cls(
            payment_id=result.payment.id,
            order_id=result.payment.order_id,
            amount=MoneySchema(
                value=result.payment.amount.value,
                currency=result.payment.amount.currency
            ),
            status=result.payment.status.value,
            created_at=result.payment.created_at,
            expires_at=result.payment.expires_at,
            confirmation_url=result.confirmation_url,
        )


class PaymentCancelResponse(BaseModel):
    payment_id: UUID
    status: str
    cancelled_at: datetime
    message: str

    @classmethod
    def from_result(cls, result: CancelPaymentResult):
        return cls(
            payment_id=result.payment.id,
            status=result.payment.status.value,
            cancelled_at=result.cancelled_at,
            message=result.message
        )


class PaymentCaptureResponse(BaseModel):
    payment_id: UUID
    status: str
    captured_at: datetime
    message: str

    @classmethod
    def from_result(cls, result: CapturePaymentResult):
        return cls(
            payment_id=result.payment.id,
            status=result.payment.status.value,
            captured_at=result.captured_at,
            message=result.message
        )


class PaymentResponse(BaseModel):
    payment_id: UUID
    order_id: UUID
    amount: MoneySchema
    payment_method: Optional[str] = None
    status: str
    created_at: datetime
    confirmation_url: str
    expires_at: Optional[datetime] = None
    captured_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None


    @classmethod
    def from_result(cls, result: PaymentWithTechnicalData):
        return cls(
            payment_id=result.payment.id,
            order_id=result.payment.order_id,
            amount=MoneySchema(
                value=result.payment.amount.value,
                currency=result.payment.amount.currency
            ),
            payment_method=result.payment_method,
            status=result.payment.status.value,
            confirmation_url=result.confirmation_url,
            created_at=result.payment.created_at,
            expires_at=result.payment.expires_at,
            captured_at=result.payment.captured_at,
            cancelled_at=result.payment.cancelled_at,
        )
