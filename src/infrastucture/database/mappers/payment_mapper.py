from typing import Optional

from src.app.dtos.payments import PaymentCreationData, CreatePaymentResult
from src.domain.payment.entities.payment import Payment
from src.domain.payment.value_objects.payment_status import PaymentStatus
from src.domain.shared.value_objects.money import Money
from src.infrastucture.database.models import PaymentORM


class PaymentDataMapper:

    @staticmethod
    def to_domain(orm_payment: PaymentORM) -> Payment:
        return Payment(
            id=orm_payment.id,
            amount=Money(
                value=orm_payment.amount,
                currency=orm_payment.currency
            ),
            status=PaymentStatus(orm_payment.status),
            order_id=orm_payment.order_id,
            created_at=orm_payment.created_at,
            captured_at=orm_payment.captured_at,
            expires_at=orm_payment.expires_at
        )

    @staticmethod
    def to_orm(
        payment_data: PaymentCreationData,
        existing_orm: Optional[PaymentORM] = None
    ) -> PaymentORM:
        payment = payment_data.payment

        if existing_orm is None:
            orm_payment = PaymentORM()
        else:
            orm_payment = existing_orm

        orm_payment.id = payment.id
        orm_payment.amount = payment.amount.value
        orm_payment.currency = payment.amount.currency
        orm_payment.status = payment.status.value
        orm_payment.order_id = payment.order_id
        orm_payment.created_at = payment.created_at
        orm_payment.captured_at = payment.captured_at
        orm_payment.expires_at = payment_data.expires_at

        # Technical fields
        orm_payment.confirmation_url = payment_data.confirmation_url
        orm_payment.payment_method = payment_data.payment_method
        orm_payment.description = payment_data.description
        orm_payment.payment_metadata = payment_data.metadata or {}
        orm_payment.idempotency_key = payment_data.idempotency_key
        orm_payment.refundable = payment_data.refundable
        orm_payment.cancelled_at = payment_data.cancelled_at

        return orm_payment

    @staticmethod
    def to_domain_with_technical_data(
        payment_orm: PaymentORM
    ) -> CreatePaymentResult:
        domain_payment = PaymentDataMapper.to_domain(payment_orm)

        return CreatePaymentResult(
            payment=domain_payment,
            confirmation_url=payment_orm.confirmation_url,
        )
