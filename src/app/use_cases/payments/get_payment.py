from uuid import UUID

from src.app.dtos.payments import PaymentWithTechnicalData
from src.domain.payment.exceptions import PaymentNotFound
from src.domain.payment.inrerfaces.ipayment_repository import IPaymentRepository


class GetPaymentUseCase:

    def __init__(self,  payment_repo: IPaymentRepository):
        self.repo = payment_repo

    async def execute(self, payment_id: UUID) -> PaymentWithTechnicalData:
        payment = await self.repo.get_with_technical_data(payment_id)

        if not payment:
            raise PaymentNotFound(
                f"Payment with {payment_id=} not found."
            )
        return payment
