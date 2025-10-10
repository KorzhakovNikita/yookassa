from src.app.dtos.payments import PaymentWithTechnicalData
from src.domain.payment.exceptions import PaymentNotFound
from src.domain.payment.inrerfaces.ipayment_repository import IPaymentRepository


class GetPaymentListUseCase:

    def __init__(self,  payment_repo: IPaymentRepository):
        self.repo = payment_repo

    async def execute(self, skip: int, limit: int) -> list[PaymentWithTechnicalData]:
        payments = await self.repo.get_all(skip, limit)

        if not payments:
            raise PaymentNotFound()

        return payments