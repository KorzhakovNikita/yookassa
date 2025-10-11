import logging
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from uuid import UUID, uuid4

from yookassa.domain.exceptions import BadRequestError
from yookassa.domain.response import PaymentResponse

from src.app.dtos.payments import PaymentCreationData, CreatePaymentResult
from src.domain.payment.entities.payment import Payment
from src.domain.payment.exceptions import PaymentGatewayError
from src.domain.payment.inrerfaces.ipayment_gateway import IPaymentGateway
from src.domain.payment.inrerfaces.ipayment_repository import IPaymentRepository
from src.domain.payment.value_objects.payment_status import PaymentStatus
from src.domain.shared.value_objects.money import Money


logger = logging.getLogger(__name__)


class CreatePaymentUseCase:

    def __init__(self, payment_repo: IPaymentRepository, payment_gateway: IPaymentGateway):
        self.repo = payment_repo
        self.payment_gateway = payment_gateway

    async def execute(
            self,
            order_id: UUID,
            amount: Money,
            description: Optional[str],
            metadata: Optional[Dict[str, Any]] = None,
            return_url: str = None
    ) -> CreatePaymentResult:

        exiting_payment = await self.repo.get_by_order_id(order_id)

        if exiting_payment and exiting_payment.payment.is_active():
            return CreatePaymentResult(
                payment=exiting_payment.payment,
                confirmation_url=exiting_payment.confirmation_url,
            )

        try:
            logger.info("Create payment request in gateway: order-id = %s", order_id)
            yookassa_response: PaymentResponse = await self.payment_gateway.create_payment(
                amount=amount,
                description=description,
                metadata=metadata,
                return_url=return_url
            )
            logger.info("Payment created in gateway successfully")

        except BadRequestError as e:
            logger.error(f"Failed to create payment in gateway: {e}")
            raise PaymentGatewayError(
                f"Failed to create payment in gateway: {str(e)}"
            )

        created_at = datetime.strptime(
            yookassa_response.created_at,
            "%Y-%m-%dT%H:%M:%S.%fZ"
        ) if yookassa_response.created_at else datetime.utcnow()
        expires_at = created_at + timedelta(minutes=10)

        payment = Payment(
            id=uuid4(),
            amount=amount,
            status=PaymentStatus.PENDING,
            order_id=order_id,
            created_at=created_at,
            expires_at=expires_at
        )

        payment_data = PaymentCreationData(
            payment=payment,
            gateway_payment_id=yookassa_response.id,
            confirmation_url=yookassa_response.confirmation.confirmation_url,
            #todo: при оплате взять payment_method
            payment_method=yookassa_response.payment_method,
            description=description,
            metadata=metadata,
            idempotency_key=uuid.uuid4()
        )

        await self.repo.save(payment_data)

        return CreatePaymentResult(
            payment=payment,
            confirmation_url=yookassa_response.confirmation.confirmation_url,
        )
