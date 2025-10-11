from typing import TypeVar, Generic, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastucture.database.base import Base

TDomain = TypeVar('TDomain')
TORM = TypeVar('TORM')
TMapper = TypeVar('TMapper')


class BaseRepository(Generic[TDomain, TORM]):

    def __init__(
        self,
        session: AsyncSession,
        orm_model: TORM,
        mapper: TMapper
    ):
        self.session = session
        self.orm_model = orm_model
        self.mapper = mapper

    async def _get_orm_by_id(self, entity_id: UUID) -> Optional[TORM]:
        query = select(self.orm_model).where(self.orm_model.id == entity_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id(self, entity_id: UUID) -> Optional[TDomain]:
        orm_model = await self._get_orm_by_id(entity_id)

        if not orm_model:
            return None

        return self.mapper.to_domain(orm_model)

    async def get_all(self, skip: int = 0, limit: int = 100):
        stmt = select(self.orm_model).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        model_orms = result.scalars().all()

        return [self.mapper.to_domain_with_technical_data(orm) for orm in model_orms]

    async def update(self, entity: TDomain):
        orm_model = await self._get_orm_by_id(entity.id)

        if not orm_model:
            raise

        self.mapper.update_orm_from_domain(orm_model, entity)
        await self.session.flush()

    async def delete(self, entity_id):
        orm_model = await self._get_orm_by_id(entity_id)

        if orm_model:
            await self.session.delete(orm_model)



