from src.domain.shared.exceptions.domain_exception import DomainException


class PaymentError(DomainException):
    pass


class InvalidPaymentStatusError(PaymentError):
    pass


class PaymentNotFound(PaymentError):
    pass


class PaymentGatewayError(PaymentError):
    pass

