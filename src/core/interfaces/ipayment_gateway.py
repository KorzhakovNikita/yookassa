from abc import ABC, abstractmethod


class IPaymentGateway(ABC):

    @abstractmethod
    async def create_payment(self, data) -> str: ...

    @abstractmethod
    async def capture_payment(self, payment_id: str): ...

    @abstractmethod
    async def cancel_payment(self, payment_id: str): ...

    @abstractmethod
    async def get_payment(self, payment_id: str): ...

    @abstractmethod
    async def get_payments(self, limit: int, offset: int): ...

    @abstractmethod
    async def get_payment_status(self, payment_id: str): ...