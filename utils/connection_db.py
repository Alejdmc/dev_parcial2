from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

# Datos de conexión a Clever Cloud (POSTGRESQL)
CLEVER_DB = (
    "postgresql+asyncpg://u2yvszfhd7jg7aaep3to:"
    "RfcLScfu3FaOP9o69x1Gf0NEuXCl5k@"
    "bay4s8hxzdohbeprhmkl-postgresql.services.clever-cloud.com:"
    "50013/bay4s8hxzdohbeprhmkl"
)

# Crear el motor de la base de datos
engine: AsyncEngine = create_async_engine(CLEVER_DB, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Inicializar la base de datos (crear tablas)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Obtener una sesión asíncrona
async def get_session():
    async with async_session() as session:
        yield session
