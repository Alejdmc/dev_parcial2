
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlmodel.ext.asyncio.session import AsyncSession
from utils.connection_db import init_db, get_session
import operations.operations_db as crud
from datas.models import Usuario, Estado_usuario


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
app = FastAPI(lifespan=lifespan)


@app.post("/usuarios/")
async def crear(usuario: Usuario, session: AsyncSession = Depends(get_session)):
    return await crud.crear_usuario(session, usuario)

@app.get("/usuarios/")
async def obtener_todos(session: AsyncSession = Depends(get_session)):
    return await crud.obtener_todos(session)

@app.get("/usuarios/{user_id}")
async def obtener_uno(user_id: int, session: AsyncSession = Depends(get_session)):
    usuario = await crud.obtener_por_id(session, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.patch("/usuarios/{user_id}/estado")
async def actualizar(user_id: int, estado: Estado_usuario, session: AsyncSession = Depends(get_session)):
    usuario = await crud.actualizar_estado(session, user_id, estado)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.patch("/usuarios/{user_id}/premium")
async def premium(user_id: int, session: AsyncSession = Depends(get_session)):
    usuario = await crud.hacer_premium(session, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.get("/usuarios/estado/{estado}")
async def por_estado(estado: Estado_usuario, session: AsyncSession = Depends(get_session)):
    return await crud.obtener_por_estado(session, estado)

@app.get("/usuarios/premium/activos")
async def premium_activos(session: AsyncSession = Depends(get_session)):
    return await crud.obtener_premium_activos(session)
