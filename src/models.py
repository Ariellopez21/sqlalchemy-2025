from datetime import datetime  
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_usuario: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    nombre: Mapped[str]
    apodo: Mapped[Optional[str]]
    ultimo_login: Mapped[Optional[datetime]]
    creado_en: Mapped[datetime] = mapped_column(default=datetime.now)
    habilitado: Mapped[bool] = mapped_column(default=True, server_default="1") # default es para python; sv_def es para postgres

    def __repr__(self) -> str:
        return f"Usuarui(id={self.id},nombre_usuario={self.nombre_usuario},apodo={self.apodo})"

