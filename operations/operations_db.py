from fastapi import Depends
from datas.models import Usuario, Estado_usuario, UsuarioCreate, Tarea, SQLModel
from sqlmodel import select, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from utils.connection_db import get_session, engine


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def crear_usuario(session: AsyncSession, usuario_create: UsuarioCreate):
    usuario = Usuario.from_orm(usuario_create)
    session.add(usuario)
    await session.commit()
    await session.refresh(usuario)
    return usuario

class TareaService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def crear_tarea(self, tarea: Tarea):
        self.session.add(tarea)
        await self.session.commit()
        await self.session.refresh(tarea)
        return tarea

async def obtener_todos(session: AsyncSession):
    result = await session.exec(select(Usuario))
    return result.all()

async def obtener_por_id(session: AsyncSession, user_id: int):
    return await session.get(Usuario, user_id)

async def actualizar_estado(session: AsyncSession, user_id: int, nuevo_estado: Estado_usuario):
    usuario = await session.get(Usuario, user_id)
    if usuario:
        usuario.estado = nuevo_estado
        await session.commit()
        await session.refresh(usuario)
    return usuario

async def hacer_premium(session: AsyncSession, user_id: int):
    usuario = await session.get(Usuario, user_id)
    if usuario:
        usuario.premium = True
        await session.commit()
        await session.refresh(usuario)
    return usuario

async def por_estado(session: AsyncSession, estado: Estado_usuario):
    result = await session.exec(select(Usuario).where(Usuario.estado == estado))
    return result.all()

async def premium_activos(session: AsyncSession):
    result = await session.exec(
        select(Usuario).where(
            Usuario.estado == Estado_usuario.activo,
            Usuario.premium == True
        )
    )
    return result.all()
