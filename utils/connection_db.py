from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

CLEVER_DB = (
    "postgresql+asyncpg://u2yvszfhd7jg7aaep3to:RfcLScfu3FaOP9o69x1Gf0NEuXCl5k@"
    "bay4s8hxzdohbeprhmkl-postgresql.services.clever-cloud.com:"
    "50013/bay4s8hxzdohbeprhmkl"
)

engine = create_async_engine(CLEVER_DB, echo=True, future=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session():
    async with async_session() as session:
        yield session
#A