from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.config.config import DATABASE_URL
from app.model.model import Base

engine = create_async_engine(
    DATABASE_URL, 
    connect_args={
        "statement_cache_size": 0,
    },)

AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
