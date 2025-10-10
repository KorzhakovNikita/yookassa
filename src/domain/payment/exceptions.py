from src.domain.shared.exceptions.domain_exception import DomainException


class PaymentError(DomainException):
    pass


class PaymentStateError(PaymentError):
    pass


class PaymentNotFound(PaymentError):
    pass


class PaymentGatewayError(PaymentError):
    pass

