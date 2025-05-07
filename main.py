
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager

from sqlalchemy.testing import db
from sqlmodel.ext.asyncio.session import AsyncSession
from utils.connection_db import init_db, get_session
import operations.operations_db as op
from datas.models import Usuario, Estado_usuario, UsuarioCreate, Tarea
from sqlmodel import Session, select

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
app = FastAPI(lifespan=lifespan)


@app.post("/usuarios/")
async def crear(usuario: UsuarioCreate, session: AsyncSession = Depends(get_session)):
    return await op.crear_usuario(session, usuario)

@app.get("/usuarios/")
async def obtener_todos(session: AsyncSession = Depends(get_session)):
    return await op.obtener_todos(session)

@app.get("/usuarios/{user_id}")
async def obtener_uno(user_id: int, session: AsyncSession = Depends(get_session)):
    usuario = await op.obtener_por_id(session, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.patch("/usuarios/{user_id}/estado")
async def actualizar(user_id: int, estado: Estado_usuario, session: AsyncSession = Depends(get_session)):
    usuario = await op.actualizar_estado(session, user_id, estado)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.patch("/usuarios/{user_id}/premium")
async def premium(user_id: int, session: AsyncSession = Depends(get_session)):
    usuario = await op.hacer_premium(session, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.get("/usuarios/estado/{estado}")
async def por_estado(estado: Estado_usuario, session: AsyncSession = Depends(get_session)):
    return await op.obtener_estado(session, estado)

@app.get("/usuarios/premium/activos")
async def premium_activos(session: AsyncSession = Depends(get_session)):
    return await op.premium_activos(session)

def get_db():
    with db.get_session() as session:
        yield session

@app.post("/tareas/", response_model=Tarea)
def crear_tarea(tarea: Tarea, db: Session = Depends(get_db)):
    db.add(tarea)
    db.commit()
    db.refresh(tarea)
    return tarea

@app.get("/tareas/", response_model=list[Tarea])
def listar_tareas(db: Session = Depends(get_db)):
    tareas = db.exec(select(Tarea)).all()
    return tareas