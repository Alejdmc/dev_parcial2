from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
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
