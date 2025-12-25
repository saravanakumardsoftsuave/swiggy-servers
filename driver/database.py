from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql+asyncpg://neondb_owner:npg_zN2gEu0XjlTk@ep-jolly-wave-a153ibmz-pooler.ap-southeast-1.aws.neon.tech/neondb?ssl=require"
engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

base = declarative_base()
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()  # ✅ Add this line
        except Exception:
            await session.rollback()
            raise