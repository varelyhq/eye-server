import os
from datetime import datetime, date

from sqlalchemy import DateTime, func, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = os.getenv('DATABASE_URL')
RESET_DB_ON_START = os.getenv('RESET_DB_ON_START', 'false').lower() == 'true'

engine = create_async_engine(DATABASE_URL, echo=False, pool_size=5, max_overflow=5)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with async_session() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        # if RESET_DB_ON_START:
        #     await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

class SerializerMixin:
    def to_dict(self) -> dict:
        result = {}
        for column in inspect(self).mapper.column_attrs:
            value = getattr(self, column.key)
            if isinstance(value, (datetime, date)):
                value = value.isoformat()
            result[column.key] = value
        return result

class TimestampMixin:
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
