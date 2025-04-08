from datetime import datetime  
from typing import Optional

from sqlalchemy import String, create_engine, select, text, not_
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# psycopg2 es el conector de bases de datos por defecto para postgres.
engine = create_engine("postgresql+psycopg:///test_db_2025", echo=False)
Session = sessionmaker(engine) 

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

def main():
    Base.metadata.create_all(engine)

    #add_users()
    #query_users()

    usuario = get_user(username="dialvarezs")
    print(usuario)

def query_users():
    with Session() as session:
        #stmt = select(Usuario).where(Usuario.apodo.is_(None)).order_by(Usuario.nombre_usuario) # Statement = stmt
        stmt = select(Usuario).order_by(Usuario.nombre_usuario.desc()) # Statement = stmt
        results = session.execute(stmt).scalars()
        
        for row in results:
            print(row)

def get_user(username: str) -> Usuario | None: 
    
    stmt = select(Usuario).where(Usuario.nombre_usuario == username)

    with Session() as session:
        result = session.execute(stmt).scalar_one_or_none()

        return result

def add_users():
    u1 = Usuario(nombre_usuario="arilopez",nombre="ariel lopez")
    u2 = Usuario(nombre_usuario="ckent",nombre="clark kent", apodo="Superman")
    u3 = Usuario(nombre_usuario="dialvarezs",nombre="Diego Alvarez S.", apodo="El Prime")

    with Session() as session:
        session.add_all([u1, u2, u3])

        print(u1.id)
        session.commit()
        print(u1.id)

if __name__ == "__main__":
    main()
