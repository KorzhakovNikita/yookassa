from abc import ABC

from src.domain.refund.entities.refund import Refund
from src.domain.shared.interfaces.repository import Repository


class IRefundRepository(Repository[Refund], ABC):
    """Abstract class for refund repo"""