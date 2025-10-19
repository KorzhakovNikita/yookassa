import logging

from src.app.dtos.payments import PaymentTechnicalDataUpdate
from src.domain.payment.exceptions import PaymentNotFound, PaymentStateError
from src.domain.payment.inrerfaces.ipayment_repository import IPaymentRepository

logger = logging.getLogger(__name__)


class HandlePaymentWaitingForCaptureUseCase:

    def __init__(self, payment_repo: IPaymentRepository):
        self.repo = payment_repo

    async def execute(self, gateway_payment_id: str, webhook_data: dict):
        logger.info(f"Processing payment.waiting_for_capture for {gateway_payment_id}")
        payment = await self.repo.get_by_gateway_payment_id(gateway_payment_id)

        if not payment:
            raise PaymentNotFound(f"Payment with id={gateway_payment_id} not found")

        if not payment.can_be_captured():
            raise PaymentStateError(
                f"Cannot capture payment with status '{payment.status.value}'. "
                f"Only payments with status PENDING that have not expired can be captured."
            )

        payment_method_data = webhook_data.get('object', {}).get('payment_method', {})
        payment_method_type = payment_method_data.get('type')

        payment.mark_as_waiting_for_capture()
        await self.repo.update(payment)

        technical_update = PaymentTechnicalDataUpdate(
            payment_method=payment_method_type
        )

        await self.repo.update_technical_fields(payment.id, technical_update)

        logger.info(f"Payment {payment.id} marked as WAITING_FOR_CAPTURE")

        return payment


