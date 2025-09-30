import logging
import traceback

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing_extensions import AsyncGenerator

from src.config import settings


logger = logging.getLogger(__name__)


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
)

SessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = SessionFactory()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        logger.error(f"Database session rolled back: {e}")
        logger.error(f"Full traceback:\n{traceback.format_exc()}")
        raise
    finally:
        await session.close()
