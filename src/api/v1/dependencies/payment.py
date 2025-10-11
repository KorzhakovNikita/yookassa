from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.use_cases.payments.cancel_payment import CancelPaymentUseCase
from src.app.use_cases.payments.capture_payment import CapturePaymentUseCase
from src.app.use_cases.payments.create_payment import CreatePaymentUseCase
from src.app.use_cases.payments.get_payment import GetPaymentUseCase
from src.app.use_cases.payments.get_payment_list import GetPaymentListUseCase
from src.app.use_cases.payments.refund_payment import RefundPaymentUseCase
from src.domain.payment.inrerfaces.ipayment_gateway import IPaymentGateway
from src.domain.payment.inrerfaces.ipayment_repository import IPaymentRepository
from src.domain.refund.interfaces.irefund_repository import IRefundRepository
from src.infrastucture.database.connection import get_session
from src.infrastucture.database.repositories.payment_repository import PaymentRepository
from src.infrastucture.database.repositories.refund_repository import RefundRepository
from src.infrastucture.yookassa.yookassa_payment_gateway import YookassaPaymentGateway


async def get_payment_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> IPaymentRepository:
    return PaymentRepository(session)


async def get_refund_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> IRefundRepository:
    return RefundRepository(session)


async def get_payment_gateway() -> IPaymentGateway:
    return YookassaPaymentGateway()


async def get_create_payment_use_case(
    payment_repo: Annotated[IPaymentRepository, Depends(get_payment_repository)],
    payment_gateway: Annotated[IPaymentGateway, Depends(get_payment_gateway)]
) -> CreatePaymentUseCase:
    return CreatePaymentUseCase(payment_repo, payment_gateway)


async def get_cancel_payment_use_case(
    payment_repo: Annotated[IPaymentRepository, Depends(get_payment_repository)],
    payment_gateway: Annotated[IPaymentGateway, Depends(get_payment_gateway)]
) -> CancelPaymentUseCase:
    return CancelPaymentUseCase(payment_repo, payment_gateway)


async def get_capture_payment_use_case(
    payment_repo: Annotated[IPaymentRepository, Depends(get_payment_repository)],
    payment_gateway: Annotated[IPaymentGateway, Depends(get_payment_gateway)]
) -> CapturePaymentUseCase:
    return CapturePaymentUseCase(payment_repo, payment_gateway)


async def get_refund_payment_use_case(
    payment_repo: Annotated[IPaymentRepository, Depends(get_payment_repository)],
    refund_repo: Annotated[IRefundRepository, Depends(get_refund_repository)],
    payment_gateway: Annotated[IPaymentGateway, Depends(get_payment_gateway)]
) -> RefundPaymentUseCase:
    return RefundPaymentUseCase(payment_repo, refund_repo, payment_gateway)


async def get_payment_use_case(
    payment_repo: Annotated[IPaymentRepository, Depends(get_payment_repository)],
) -> GetPaymentUseCase:
    return GetPaymentUseCase(payment_repo)


async def get_payment_list_use_case(
    payment_repo: Annotated[IPaymentRepository, Depends(get_payment_repository)],
) -> GetPaymentListUseCase:
    return GetPaymentListUseCase(payment_repo)


