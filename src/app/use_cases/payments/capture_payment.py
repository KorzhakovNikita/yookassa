import logging
from uuid import UUID

from yookassa.domain.response import PaymentResponse

from src.app.dtos.payments import CapturePaymentResult
from src.domain.payment.exceptions import PaymentError, PaymentGatewayError, PaymentNotFound, PaymentStateError
from src.domain.payment.inrerfaces.ipayment_gateway import IPaymentGateway
from src.domain.payment.inrerfaces.ipayment_repository import IPaymentRepository


logger = logging.getLogger(__name__)


class CapturePaymentUseCase:

    def __init__(self, payment_repo: IPaymentRepository, payment_gateway: IPaymentGateway):
        self.repo = payment_repo
        self.gateway = payment_gateway

    async def execute(self, payment_id: UUID) -> CapturePaymentResult:
        existing_payment = await self.repo.get_with_technical_data(payment_id)

        if not existing_payment:
            raise PaymentNotFound(f"Payment with id={payment_id} not found.")

        payment = existing_payment.payment
        gateway_payment_id = existing_payment.gateway_payment_id

        if not payment.can_be_captured():
            raise PaymentStateError(
                f"Cannot cancel payment with status '{payment.status.value}'. "
                f"Only payments with status WAITING_FOR_CAPTURE that have not expired can be captured."
            )

        try:
            logger.info(f"Capture payment in gateway: {gateway_payment_id}")
            yookassa_response: PaymentResponse = await self.gateway.capture_payment(gateway_payment_id)
            logger.info(f"Payment captured in gateway successfully")

        except Exception as e:
            logger.error(f"Failed to capture payment in gateway: {e}")
            raise PaymentGatewayError(
                f"Failed to capture payment in gateway: {str(e)}"
            )

        payment.mark_as_captured()
        await self.repo.update(payment)

        return CapturePaymentResult(
            payment=payment,
            captured_at=payment.captured_at
        )
