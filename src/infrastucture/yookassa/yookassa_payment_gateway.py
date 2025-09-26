from src.core.interfaces.ipayment_gateway import IPaymentGateway
from src.config import settings


class YookassaPaymentGateway(IPaymentGateway):

    def __init__(self):
        #todo: settings
        self.shop_id = settings.SHOP_ID
        self.secret_key = settings.SHOP_SECRET_KEY

    async def create_payment(self, data) -> str:
        pass

    async def capture_payment(self, payment_id: str) -> bool:
        pass

    async def cancel_payment(self, payment_id: str) -> bool:
        pass

    async def get_payment(self, payment_id: str):
        pass

    async def get_payments(self, limit: int, offset: int):
        pass

    async def get_payment_status(self, payment_id: str) -> str:
        pass
