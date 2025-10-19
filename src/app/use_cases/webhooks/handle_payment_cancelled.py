import logging

from src.domain.payment.exceptions import PaymentNotFound, PaymentStateError
from src.domain.payment.inrerfaces.ipayment_repository import IPaymentRepository

logger = logging.getLogger(__name__)


class HandlePaymentCanceledUseCase:

    def __init__(self, payment_repo: IPaymentRepository):
        self.repo = payment_repo

    async def execute(self, gateway_payment_id: str, webhook_data: dict):
        logger.info(f"Processing payment.cancelled for {gateway_payment_id}")

        payment = await self.repo.get_by_gateway_payment_id(gateway_payment_id)

        if not payment:
            raise PaymentNotFound(f"Payment with id={gateway_payment_id} not found")

        if not payment.can_be_cancelled():
            raise PaymentStateError(
                f"Cannot cancel payment with status '{payment.status.value}'. "
                f"Only payments with status WAITING_FOR_CAPTURE that have not expired can be captured."
            )

        payment.mark_as_cancelled()
        await self.repo.update(payment)

        logger.info(f"Payment {payment.id} marked as CANCELLED")

        return payment


