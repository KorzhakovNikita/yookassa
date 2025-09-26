from abc import ABC, abstractmethod
from typing import Optional

from src.core.entities.payment import Payment


class IPaymentRepository(ABC):

    @abstractmethod
    async def get_by_id(self, payment_id: str) -> Optional[Payment]:  ...

    @abstractmethod
    async def get_by_order_id(self, order_id: str) -> Optional[Payment]: ...

    @abstractmethod
    async def save(self, payment: Payment) -> None: ...

    @abstractmethod
    async def list_by_user_id(self, user_id: str) -> list[Payment]: ...

