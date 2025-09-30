from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.use_cases.payments.create_payment import CreatePaymentUseCase
from src.domain.payment.inrerfaces.ipayment_gateway import IPaymentGateway
from src.domain.payment.inrerfaces.ipayment_repository import IPaymentRepository
from src.infrastucture.database.connection import get_session
from src.infrastucture.database.repositories.payment_repository import PaymentRepository
from src.infrastucture.yookassa.yookassa_payment_gateway import YookassaPaymentGateway


async def get_payment_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> IPaymentRepository:
    return PaymentRepository(session)


async def get_payment_gateway() -> IPaymentGateway:
    return YookassaPaymentGateway()


async def get_create_payment_use_case(
    payment_repo: Annotated[IPaymentRepository, Depends(get_payment_repository)],
    payment_gateway: Annotated[IPaymentGateway, Depends(get_payment_gateway)]
) -> CreatePaymentUseCase:
    return CreatePaymentUseCase(payment_repo, payment_gateway)
