from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.dtos.payments import PaymentCreationData, CreatePaymentResult
from src.domain.payment.entities.payment import Payment
from src.domain.payment.exceptions import PaymentNotFound
from src.domain.payment.inrerfaces.ipayment_repository import IPaymentRepository
from src.infrastucture.database.mappers.payment_mapper import PaymentDataMapper
from src.infrastucture.database.models import PaymentORM


class PaymentRepository(IPaymentRepository):

    def __init__(self, session: AsyncSession):
        self.session = session
        self.mapper = PaymentDataMapper()

    async def get_by_id(self, payment_id: UUID) -> Optional[Payment]:
        payment = await self._get_by_id(payment_id)

        if payment is None:
            raise PaymentNotFound(f"Payment with id={payment_id} not found.")

        return PaymentDataMapper.to_domain(payment)

    async def get_by_order_id(self, order_id: UUID) -> Optional[CreatePaymentResult]:
        query = (
            select(PaymentORM)
            .where(PaymentORM.order_id == order_id)
            .order_by(PaymentORM.created_at.desc())
            .limit(1)
        )
        result = await self.session.execute(query)
        payment_orm = result.scalars().first()

        return self.mapper.to_domain_with_technical_data(payment_orm) if payment_orm else None

    async def save(self, data: PaymentCreationData) -> None:
        existing_orm = None
        payment_id = data.payment.id

        if payment_id:
            existing_orm = await self._get_by_id(payment_id)

        orm_payment = self.mapper.to_orm(data, existing_orm)

        if existing_orm is None:
            self.session.add(orm_payment)

        await self.session.flush()

    async def delete(self, payment: Payment) -> None:
        payment_orm = await self._get_by_id(payment.id)

        if payment_orm:
            await self.session.delete(payment_orm)

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[Payment]:
        stmt = select(PaymentORM).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        payments_orm = result.scalars().all()

        return [self.mapper.to_domain(payment) for payment in payments_orm]

    async def _get_by_id(self, payment_id: UUID) -> PaymentORM:
        stmt = select(PaymentORM).where(PaymentORM.id == payment_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
