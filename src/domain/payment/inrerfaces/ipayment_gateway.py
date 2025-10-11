from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from yookassa.domain.response import PaymentResponse

from src.domain.shared.value_objects.money import Money


class IPaymentGateway(ABC):

    @abstractmethod
    async def create_payment(
            self,
            amount: Money,
            description: Optional[str],
            metadata: Optional[Dict[str, Any]] = None,
            return_url: str = None
    ) -> PaymentResponse: ...

    @abstractmethod
    async def capture_payment(self, payment_id: str) -> PaymentResponse: ...

    @abstractmethod
    async def cancel_payment(self, payment_id: str) -> PaymentResponse: ...

    @abstractmethod
    async def refund_payment(self, payment_id: str, value: float, currency: str) -> PaymentResponse: ...

    @abstractmethod
    async def get_payment(self, payment_id: str): ...

    @abstractmethod
    async def get_payments(self, limit: int, offset: int): ...

    @abstractmethod
    async def get_payment_status(self, payment_id: str): ...