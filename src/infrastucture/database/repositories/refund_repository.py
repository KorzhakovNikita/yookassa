from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.dtos.refunds import RefundCreationData
from src.domain.refund.entities.refund import Refund
from src.domain.refund.interfaces.irefund_repository import IRefundRepository
from src.infrastucture.database.mappers.refund_mapper import RefundDataMapper
from src.infrastucture.database.models import RefundORM
from src.infrastucture.database.repositories.base_repository import BaseRepository


class RefundRepository(BaseRepository[RefundORM, Refund], IRefundRepository):

    def __init__(self, session: AsyncSession):

        super().__init__(
            session=session,
            orm_model=RefundORM,
            mapper=RefundDataMapper()
        )

    async def save(self, data: RefundCreationData) -> None:
        existing_orm = None
        refund_id = data.refund.id

        if refund_id:
            existing_orm = await self._get_orm_by_id(refund_id)

        orm_refund = self.mapper.to_orm(data, existing_orm)

        if existing_orm is None:
            self.session.add(orm_refund)

        await self.session.flush()

    async def get_by_gateway_refund_id(self, gateway_refund_id: str) -> Optional[Refund]:
        query = (
            select(RefundORM)
            .where(RefundORM.gateway_refund_id == gateway_refund_id)
            .order_by(RefundORM.created_at.desc())
            .limit(1)
        )
        result = await self.session.execute(query)
        refund_orm = result.scalars().first()

        return self.mapper.to_domain(refund_orm) if refund_orm else None
