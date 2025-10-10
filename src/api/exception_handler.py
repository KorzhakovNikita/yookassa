from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.domain.payment.exceptions import PaymentNotFound, PaymentStateError, PaymentGatewayError


async def payment_not_found_handler(request: Request, exc: PaymentNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "payment_not_found",
            "message": str(exc)
        }
    )


async def payment_state_error_handler(request: Request, exc: PaymentStateError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "payment_state_error",
            "message": str(exc)
        }
    )


async def payment_gateway_error_handler(request: Request, exc: PaymentGatewayError):
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={
            "error": "payment_gateway_error",
            "message": str(exc)
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "internal_server_error",
            "message": f"An unexpected error occurred: {str(exc)}"
        }
    )