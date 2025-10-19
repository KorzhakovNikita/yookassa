import logging

from src.domain.payment.exceptions import PaymentNotFound, PaymentStateError
from src.domain.payment.inrerfaces.ipayment_repository import IPaymentRepository
from src.domain.payment.value_objects.payment_status import PaymentStatus
from src.domain.refund.interfaces.irefund_repository import IRefundRepository
from src.domain.refund.value_objects.refund_status import RefundStatus

logger = logging.getLogger(__name__)


class HandleRefundSucceededUseCase:

    def __init__(self, payment_repo: IPaymentRepository, refund_repo: IRefundRepository,):
        self.payment_repo = payment_repo
        self.refund_repo = refund_repo

    async def execute(self, gateway_refund_id: str, webhook_data: dict):
        logger.info(f"Processing refund.succeeded for {gateway_refund_id}")
        refund = await self.refund_repo.get_by_gateway_refund_id(gateway_refund_id)

        if not refund:
            raise PaymentNotFound(f"Refund with gateway_refund_id={gateway_refund_id} not found")

        if refund.status == RefundStatus.SUCCEEDED:
            logger.warning(f"Refund {refund.id} already succeeded, skipping")
            return refund

        refund.mark_as_succeeded()
        await self.refund_repo.update(refund)

        payment_data = await self.payment_repo.get_with_technical_data(refund.payment_id)
        payment = payment_data.payment

        if payment.status != PaymentStatus.SUCCEEDED:
            logger.warning(
                f"Payment {payment.id} is not SUCCEEDED (current: {payment.status}), "
                "but refund completed"
            )
            payment.mark_as_refunded()

        await self.payment_repo.update(payment)

        logger.info(f"Payment {payment.id} marked as REFUND")

        return payment


