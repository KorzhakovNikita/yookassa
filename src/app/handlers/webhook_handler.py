import logging
from typing import Callable, Any, Optional

from yookassa.domain.notification import WebhookNotificationFactory

from src.app.enums.webhook_events import WebhookEventType

logger = logging.getLogger(__name__)


class WebhookHandler:

    def __init__(self, use_cases: dict[WebhookEventType, Callable]):
        self.use_cases = use_cases

    async def handle(self, webhook_data: dict[str, Any]):
        notification_object = WebhookNotificationFactory().create(webhook_data)
        response_object = notification_object.object
        event_type = self._get_event_type(webhook_data.get("event"))
        print(f"\n{event_type=}\n")
        use_case = self.use_cases.get(event_type)
        print(f"\n{use_case=}\n")

        if not use_case:
            logger.warning("No handler for event: %s", event_type)
            return {"status": "ignored", "event": event_type} #400

        result = await use_case.execute(
            response_object.id,
            webhook_data=webhook_data
        )
        return {"status": "ok"}

    def _get_event_type(self, event: str) -> Optional[WebhookEventType]:
        try:
            return WebhookEventType(event)
        except ValueError:
            return None

