
class DomainPaymentException(Exception):
    pass


class InvalidPaymentStatusError(DomainPaymentException):
    pass
