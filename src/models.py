from datetime import datetime  
from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

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

    emails: Mapped[list["Email"]] = relationship(back_populates="usuario")
    grupos: Mapped[list["Grupo"]] = relationship(back_populates="usuarios", secondary="usuarios_grupos")

    def __repr__(self) -> str:
        return f"Usuarui(id={self.id},nombre_usuario={self.nombre_usuario},apodo={self.apodo})"

class Email(Base):
    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))

    usuario: Mapped["Usuario"] = relationship(back_populates="emails")

    def __repr__(self) -> str:
        return f"Email(id={self.id},email={self.email})"
    

class Grupo(Base):
    __tablename__ = "grupos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    
    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="grupos", secondary="usuarios_grupos")

    def __repr__(self) -> str:
        return f"Grupo(id={self.id},nombre={self.nombre})"

class UsuarioGrupo(Base):
    __tablename__ = "usuarios_grupos"

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), primary_key=True) 
    grupo_id: Mapped[int] = mapped_column(ForeignKey("grupos.id"), primary_key=True)
