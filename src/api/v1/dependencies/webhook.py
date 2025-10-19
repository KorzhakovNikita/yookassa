from typing import Annotated

from fastapi import Depends

from src.api.v1.dependencies.payment import get_payment_repository, get_refund_repository
from src.app.enums.webhook_events import WebhookEventType
from src.app.handlers.webhook_handler import WebhookHandler
from src.app.use_cases.webhooks.handle_payment_cancelled import HandlePaymentCanceledUseCase
from src.app.use_cases.webhooks.handle_payment_succeeded import HandlePaymentSucceededUseCase
from src.app.use_cases.webhooks.handle_payment_waiting_for_capture import HandlePaymentWaitingForCaptureUseCase
from src.app.use_cases.webhooks.handle_refund_succeeded import HandleRefundSucceededUseCase
from src.domain.payment.inrerfaces.ipayment_repository import IPaymentRepository
from src.domain.refund.interfaces.irefund_repository import IRefundRepository


async def get_webhook_handler(
        payment_repo: Annotated[IPaymentRepository, Depends(get_payment_repository)],
        refund_repo: Annotated[IRefundRepository, Depends(get_refund_repository)]
) -> WebhookHandler:
    use_cases = {
        WebhookEventType.PAYMENT_SUCCEEDED:
            HandlePaymentSucceededUseCase(payment_repo),

        WebhookEventType.PAYMENT_WAITING_FOR_CAPTURE:
            HandlePaymentWaitingForCaptureUseCase(payment_repo),

        WebhookEventType.PAYMENT_CANCELED:
            HandlePaymentCanceledUseCase(payment_repo),

        WebhookEventType.REFUND_SUCCEEDED:
            HandleRefundSucceededUseCase(payment_repo, refund_repo),
    }

    return WebhookHandler(use_cases)