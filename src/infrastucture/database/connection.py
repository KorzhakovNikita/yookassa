import logging
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing_extensions import AsyncGenerator

from src.config import settings


logger = logging.getLogger(__name__)


class Database:

    def __init__(self):
        self.engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DATABASE_ECHO,
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
            pool_pre_ping=settings.DATABASE_POOL_PRE_PING,
        )

        self.session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

        logger.info("DatabaseManager initialized")

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        session = self.session_factory()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session rolled back: {e}")
            raise
        finally:
            await session.close()
