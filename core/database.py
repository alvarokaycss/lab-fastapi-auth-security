from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine

from core.settings import settings

engine: AsyncEngine = create_async_engine(url=settings.DB_URL) 

SessionLocal = sessionmaker(
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)
