from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enum import Enum

class Estado_usuario(str, Enum):
    activo = "Activo"
    inactivo = "Inactivo"
    eliminado = "Eliminado"

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    apellido: str
    email: str
    password: str
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    fecha_modificacion: datetime = Field(default_factory=datetime.now)
    estado: Estado_usuario = Field(default=Estado_usuario.activo)
    premium: bool = Field(default=False)

    tareas: List["Tarea"] = Relationship(back_populates="usuario")

class EstadoTareaEnum(str, Enum):
    pendiente = "Pendiente"
    en_ejecucion = "En ejecución"
    realizada = "Realizada"
    cancelada = "Cancelada"

class Tarea(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    estado: EstadoTareaEnum
    usuario_id: int = Field(foreign_key="usuario.id")
    usuario: Optional[Usuario] = Relationship(back_populates="tareas")

class UsuarioCreate(SQLModel):
    nombre: str
    apellido: str
    email: str
    password: str

    class Config:
        orm_mode = True
