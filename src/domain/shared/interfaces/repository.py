from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from uuid import UUID

T = TypeVar('T')


class Repository(ABC, Generic[T]):
    """Base interface repository"""

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[T]: ...

    @abstractmethod
    async def save(self, data) -> None: ...

    @abstractmethod
    async def update(self, entity: T) -> None: ...

    @abstractmethod
    async def delete(self, entity: T) -> None: ...

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> Optional[List[T]]: ...