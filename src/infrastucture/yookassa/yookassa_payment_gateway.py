from typing import Optional, Dict, Any

from yookassa import Payment, Configuration

from src.domain.payment.inrerfaces.ipayment_gateway import IPaymentGateway
from src.config import settings
from src.domain.shared.value_objects.money import Money


class YookassaPaymentGateway(IPaymentGateway):

    def __init__(self):
        # todo: main.py startup or class implementation
        self.shop_id = settings.SHOP_ID
        self.secret_key = settings.SHOP_SECRET_KEY

    async def create_payment(
            self,
            amount: Money,
            description: Optional[str],
            metadata: Optional[Dict[str, Any]] = None,
            return_url: str = None
    ) -> str:
        payment = Payment.create(
            {
                "amount": {
                    "value": amount.value,
                    "currency": amount.currency
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": return_url
                },
                "capture": False,
                "description": description,
                "metadata": metadata
            }
        )
        return payment

    async def capture_payment(self, payment_id: str) -> bool:
        capture_response = Payment.capture(payment_id)
        return capture_response

    async def cancel_payment(self, payment_id: str) -> bool:
        # todo: нужен ли тут ключ idempotency_key
        cancel_response = Payment.cancel(payment_id)
        return cancel_response

    async def get_payment(self, payment_id: str):
        pass

    async def get_payments(self, limit: int, offset: int):
        pass

    async def get_payment_status(self, payment_id: str) -> str:
        pass
