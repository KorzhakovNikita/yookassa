import logging
import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from yookassa.domain.exceptions import BadRequestError

from src.app.dtos.refunds import RefundPaymentResult, RefundCreationData
from src.domain.payment.exceptions import PaymentNotFound, PaymentStateError, PaymentGatewayError
from src.domain.payment.inrerfaces.ipayment_gateway import IPaymentGateway
from src.domain.payment.inrerfaces.ipayment_repository import IPaymentRepository
from src.domain.refund.entities.refund import Refund
from src.domain.refund.interfaces.irefund_repository import IRefundRepository
from src.domain.refund.value_objects.refund_status import RefundStatus
from src.domain.shared.value_objects.money import Money

logger = logging.getLogger(__name__)


class RefundPaymentUseCase:

    def __init__(
            self, payment_repo: IPaymentRepository, refund_repo: IRefundRepository, payment_gateway: IPaymentGateway
    ):
        self.payment_repo = payment_repo
        self.refund_repo = refund_repo
        self.gateway = payment_gateway

    async def execute(self, payment_id: UUID, reason: Optional[str]) -> RefundPaymentResult:
        existing_payment = await self.payment_repo.get_with_technical_data(payment_id)

        if not existing_payment:
            raise PaymentNotFound(f"Payment with id={payment_id} not found")

        payment = existing_payment.payment
        gateway_payment_id = existing_payment.gateway_payment_id

        if not payment.can_be_refund():
            raise PaymentStateError(
                f"Cannot refund payment with status '{payment.status.value}'. "
                f"Only payments with status SUCCEEDED that have not expired can be refunded."
            )

        refund = Refund(
            id=uuid.uuid4(),
            payment_id=payment.id,
            amount=Money(
                value=payment.amount.value,
                currency=payment.amount.currency
            ),
            status=RefundStatus.PENDING,
            reason=reason,
            created_at=datetime.utcnow()
        )

        try:
            logger.info(f"Refund payment in gateway: {gateway_payment_id}")
            yookassa_response = await self.gateway.refund_payment(
                gateway_payment_id, payment.amount.value, payment.amount.currency
            )
            #todo: cancellation_details handle with reason

            logger.info(f"Payment captured in gateway successfully")
        except BadRequestError as e:
            logger.error(f"Failed to refund payment in gateway: {e}")
            raise PaymentGatewayError(
                f"Failed to refund payment in gateway: {str(e)}"
            )

        payment.mark_as_refunded()
        await self.payment_repo.update(payment)

        refund_data = RefundCreationData(
            refund=refund,
            gateway_refund_id=yookassa_response.id
        )
        refund.mark_as_succeeded()
        await self.refund_repo.save(refund_data)

        return RefundPaymentResult(
            payment=payment,
            refund=refund,
            refunded_amount=refund.amount
        )


