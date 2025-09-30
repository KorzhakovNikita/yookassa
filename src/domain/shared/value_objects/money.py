from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class Money:
    value: float
    currency: str

    SUPPORTED_CURRENCIES: ClassVar[list] = ["RUB", "USD", "EUR"]

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Money amount cannot be negative")
        if self.currency not in self.SUPPORTED_CURRENCIES:
            raise ValueError(f"Unsupported currency: {self.currency}")
