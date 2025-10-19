from typing import Annotated

from fastapi import Request, Depends, APIRouter, HTTPException

from src.api.v1.dependencies.webhook import get_webhook_handler
from src.app.handlers.webhook_handler import WebhookHandler
from src.domain.payment.exceptions import PaymentNotFound

router = APIRouter(prefix="/v1/webhooks", tags=["Webhook"])


@router.post("/yookassa")
async def yookassa_webhook(
    request: Request,
    handler: Annotated[WebhookHandler, Depends(get_webhook_handler)]
):

    try:
        webhook_data = await request.json()
        result = await handler.handle(webhook_data)
        return result
    except PaymentNotFound:
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=500)
