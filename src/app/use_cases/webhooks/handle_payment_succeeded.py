import logging

from src.domain.payment.exceptions import PaymentNotFound, PaymentStateError
from src.domain.payment.inrerfaces.ipayment_repository import IPaymentRepository

logger = logging.getLogger(__name__)


class HandlePaymentSucceededUseCase:

    def __init__(self, payment_repo: IPaymentRepository):
        self.repo = payment_repo

    async def execute(self, gateway_payment_id: str, webhook_data: dict):
        logger.info(f"Processing payment.succeeded for {gateway_payment_id}")

        payment = await self.repo.get_by_gateway_payment_id(gateway_payment_id)

        if not payment:
            raise PaymentNotFound(f"Payment with id={gateway_payment_id} not found")

        if not payment.can_be_succeeded():
            raise PaymentStateError(
                f"Cannot succeeded payment with status '{payment.status.value}'. "
                f"Only payments with status WAITING_FOR_CAPTURE that have not expired can be captured."
            )

        # todo: достать из webhook_data
        # mark_as_succeeded
        payment.mark_as_captured()
        await self.repo.update(payment)

        logger.info(f"Payment {payment.id} marked as SUCCEEDED")

        return payment


