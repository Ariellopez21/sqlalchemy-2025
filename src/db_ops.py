from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.db import Session, engine
from src.models import Base, Usuario

def query_users():
    with Session() as session:
        #stmt = select(Usuario).where(Usuario.apodo.is_(None)).order_by(Usuario.nombre_usuario) # Statement = stmt
        stmt = select(Usuario) # Statement = stmt
        stmt.order_by(Usuario.nombre_usuario.desc()) # Statement = stmt

        results = session.execute(stmt).scalars().fetchall()
        
        return results

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

def disable_user(username: str) -> None:
    
    with Session() as session:
        with session.begin():
            try: 
                user = session.execute(select(Usuario).where(Usuario.nombre_usuario == username)).scalar_one()

                user.habilitado = False
            except NoResultFound:
                print(f"User {username} not found")

def create_database():
    Base.metadata.create_all(engine)