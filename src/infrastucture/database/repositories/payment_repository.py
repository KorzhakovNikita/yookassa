from typing import Optional

from src.core.entities.payment import Payment
from src.core.interfaces.ipayment_repository import IPaymentRepository


class PaymentRepository(IPaymentRepository):

    def __init__(self, session):
        self.session = session

    async def get_by_id(self, payment_id: str) -> Optional[Payment]:
        pass

    async def get_by_order_id(self, order_id: str) -> Optional[Payment]:
        pass

    async def save(self, payment: Payment) -> None:
        pass

    async def list_by_user_id(self, user_id: str) -> list[Payment]:
        pass