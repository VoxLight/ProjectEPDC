from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .models import Base
from EPDCBot.utils import Config

class DatabaseConnection:
    def __init__(self):
        self.engine = create_async_engine(Config.DATABASE_URI(), echo=True, future=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, class_=AsyncSession)

    # async with DBManager().get_session() as session: # for context manager.
    async def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
        finally:
            await session.close()

    async def setup(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def teardown(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    
    