from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.dtos.payments import PaymentCreationData, CreatePaymentResult, PaymentWithTechnicalData, \
    PaymentTechnicalDataUpdate
from src.domain.payment.entities.payment import Payment
from src.domain.payment.exceptions import PaymentNotFound
from src.domain.payment.inrerfaces.ipayment_repository import IPaymentRepository
from src.infrastucture.database.mappers.payment_mapper import PaymentDataMapper
from src.infrastucture.database.models import PaymentORM
from src.infrastucture.database.repositories.base_repository import BaseRepository


class PaymentRepository(BaseRepository[Payment, PaymentORM], IPaymentRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            orm_model=PaymentORM,
            mapper=PaymentDataMapper()
        )

    async def get_with_technical_data(self, payment_id: UUID) -> Optional[PaymentWithTechnicalData]:
        payment = await self._get_orm_by_id(payment_id)
        return self.mapper.to_domain_with_technical_data(payment)

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
            existing_orm = await self._get_orm_by_id(payment_id)

        orm_payment = self.mapper.to_orm(data, existing_orm)

        if existing_orm is None:
            self.session.add(orm_payment)

        await self.session.flush()

    async def get_by_gateway_payment_id(self, gateway_payment_id: str) -> Optional[Payment]:
        query = (
            select(PaymentORM)
            .where(PaymentORM.gateway_payment_id == gateway_payment_id)
            .order_by(PaymentORM.created_at.desc())
            .limit(1)
        )
        result = await self.session.execute(query)
        payment_orm = result.scalars().first()

        return self.mapper.to_domain(payment_orm) if payment_orm else None

    async def update_technical_fields(self, payment_id: UUID, technical_data: PaymentTechnicalDataUpdate) -> None:
        orm_payment = await self._get_orm_by_id(payment_id)

        if not orm_payment:
            raise PaymentNotFound(f"Payment {payment_id} not found")

        technical_data.apply_to_orm(orm_payment)

        await self.session.flush()
