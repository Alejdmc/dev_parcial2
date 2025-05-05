from datas.models import Usuario, Estado_usuario, UsuarioCreate
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


async def crear_usuario(session: AsyncSession, usuario_create: UsuarioCreate):
    usuario = Usuario.from_orm(usuario_create)
    session.add(usuario)
    await session.commit()
    await session.refresh(usuario)
    return usuario

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

async def obtener_por_estado(session: AsyncSession, estado: Estado_usuario):
    result = await session.exec(select(Usuario).where(Usuario.estado == estado))
    return result.all()

async def obtener_premium_activos(session: AsyncSession):
    result = await session.exec(
        select(Usuario).where(
            Usuario.estado == Estado_usuario.activo,
            Usuario.premium == True
        )
    )
    return result.all()
