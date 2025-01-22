from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from config.config import DATABASE_URL

engine = create_async_engine(url=DATABASE_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)

async def get_session():
    async with async_session_maker() as session:
        yield session

class Base(DeclarativeBase):
    __abstract__=True
