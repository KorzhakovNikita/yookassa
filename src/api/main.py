import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from yookassa import Configuration

from src.config import settings
from src.api.v1.routers.payments import router as payment_router

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


@app.on_event("startup")
async def startup_event():
    Configuration.configure(settings.SHOP_ID, settings.SHOP_SECRET_KEY)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
        proxy_headers=True,
    )
