from abc import ABC, abstractmethod
from typing import Optional

from src.domain.refund.entities.refund import Refund
from src.domain.shared.interfaces.repository import Repository


class IRefundRepository(Repository[Refund], ABC):
    """Abstract class for refund repo"""

    @abstractmethod
    async def get_by_gateway_refund_id(self, gateway_payment_id: str) -> Optional[Refund]: ...