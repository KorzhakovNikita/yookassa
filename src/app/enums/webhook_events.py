from enum import Enum


class WebhookEventType(str, Enum):
    PAYMENT_SUCCEEDED = "payment.succeeded"
    PAYMENT_WAITING_FOR_CAPTURE = "payment.waiting_for_capture"
    PAYMENT_CANCELED = "payment.canceled"
    REFUND_SUCCEEDED = "refund.succeeded"

