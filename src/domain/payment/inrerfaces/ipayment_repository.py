from abc import abstractmethod
from typing import Optional
from uuid import UUID

from src.app.dtos.payments import CreatePaymentResult
from src.domain.payment.entities.payment import Payment
from src.domain.shared.interfaces.repository import Repository


class IPaymentRepository(Repository[Payment]):

    @abstractmethod
    async def get_by_order_id(self, order_id: UUID) -> Optional[CreatePaymentResult]: ...



