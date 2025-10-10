import logging
from uuid import UUID

from yookassa.domain.exceptions import BadRequestError

from src.app.dtos.payments import CancelPaymentResult
from src.domain.payment.exceptions import PaymentError, PaymentGatewayError, PaymentNotFound, PaymentStateError
from src.domain.payment.inrerfaces.ipayment_gateway import IPaymentGateway
from src.domain.payment.inrerfaces.ipayment_repository import IPaymentRepository


logger = logging.getLogger(__name__)


class CancelPaymentUseCase:

    def __init__(self, payment_repo: IPaymentRepository, payment_gateway: IPaymentGateway):
        self.repo = payment_repo
        self.payment_gateway = payment_gateway

    async def execute(self, payment_id: UUID):
        existing_payment = await self.repo.get_with_technical_data(payment_id)

        if not existing_payment:
            raise PaymentNotFound(f"Payment with id={payment_id} not found.")

        payment = existing_payment.payment
        gateway_payment_id = existing_payment.gateway_payment_id

        if not payment.can_be_cancelled():
            raise PaymentStateError(
                f"Cannot cancel payment with status '{payment.status.value}'. "
                f"Only payments with status WAITING_FOR_CAPTURE that have not expired can be cancelled."
            )

        try:
            logger.info(f"Cancelling payment in gateway: {gateway_payment_id}")
            yookassa_response = await self.payment_gateway.cancel_payment(gateway_payment_id)
            logger.info(f"Payment cancelled in gateway successfully")

        except BadRequestError as e:
            logger.error(f"Failed to cancel payment in gateway: {str(e)}")
            raise PaymentGatewayError(
                f"Failed to cancel payment in gateway: {str(e)}"
            )

        payment.mark_as_cancelled()

        await self.repo.update(payment)

        logger.info(f"Payment {payment_id} cancelled successfully")

        return CancelPaymentResult(
            payment=payment,
            cancelled_at=payment.cancelled_at,
        )