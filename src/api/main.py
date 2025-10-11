import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from yookassa import Configuration

from src.api.exception_handler import payment_not_found_handler, payment_state_error_handler, \
    payment_gateway_error_handler, general_exception_handler
from src.config import settings, configure_logging
from src.api.v1.routers.payments import router as payment_router
from src.domain.payment.exceptions import PaymentNotFound, PaymentStateError, PaymentGatewayError

app = FastAPI(title="YookassaService")

app.include_router(payment_router)
# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handlers
app.add_exception_handler(PaymentNotFound, payment_not_found_handler)
app.add_exception_handler(PaymentStateError, payment_state_error_handler)
app.add_exception_handler(PaymentGatewayError, payment_gateway_error_handler)
app.add_exception_handler(Exception, general_exception_handler)


@app.on_event("startup")
async def startup_event():
    configure_logging()
    Configuration.configure(settings.SHOP_ID, settings.SHOP_SECRET_KEY)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
        proxy_headers=True,
    )
