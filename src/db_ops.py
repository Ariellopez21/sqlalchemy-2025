from ssl import SSLSession
from typing import Sequence
from faker import Faker
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from src.db import Session, engine
from src.models import Base, Usuario, Email, Grupo


def query_users() :
    with Session() as session:
        #stmt = select(Usuario).where(Usuario.apodo.is_(None)).order_by(Usuario.nombre_usuario) # Statement = stmt
        stmt = select(Usuario) # Statement = stmt
        stmt.order_by(Usuario.nombre_usuario.desc()) # Statement = stmt

        results = session.execute(stmt).scalars().fetchall()
        
        return results

def get_user(username: str, session) -> Usuario | None: 
    
    stmt = (
        select(Usuario)
        #.options(selectinload(Usuario.emails))
        .where(Usuario.nombre_usuario == username)
        )

    user = session.execute(stmt).scalar_one_or_none()

    return user

def add_users():
    #u1 = Usuario(nombre_usuario="arilopez",nombre="ariel lopez")
    u2 = Usuario(nombre_usuario="ckent",nombre="clark kent", apodo="Superman")
    u3 = Usuario(nombre_usuario="dialvarezs",nombre="Diego Alvarez S.", apodo="El Prime")

    with Session() as session:
        session.add_all([u2, u3])

        session.commit()


def disable_user(username: str) -> None:
    with Session() as session:
        with session.begin():
            try: 
                user = session.execute(select(Usuario).where(Usuario.nombre_usuario == username)).scalar_one()

                user.habilitado = False
            except NoResultFound:
                print(f"User {username} not found")

def turn_enabled_users(usernames: list[str], is_habilitado=True) -> None:
    with Session() as session:
        with session.begin():
            stmt = (
                update(Usuario)
                .where(Usuario.nombre_usuario.in_(usernames))
                .values(habilitado=is_habilitado)
            )
            session.execute(stmt)

def delete_user(username: str) -> None:
    with Session() as session:
        with session.begin():
            try: 
                user = session.execute(select(Usuario).where(Usuario.nombre_usuario == username)).scalar_one()
                session.delete(user)
                
            except NoResultFound:
                print(f"User {username} not found")

def add_email_to_user(username: str, email: str) -> None:
    with Session() as session:
        with session.begin():
            user = session.execute(
                select(Usuario).where(Usuario.nombre_usuario == username)
            ).scalar_one()
            user.emails.append(Email(email=email))

# YA NO SIRVE PORQUE LO SUSTITUYE EMAILS DE MODELS.PY
def get_user_emails(username: str) -> Sequence[Email]:
    with Session() as session:
        user = session.execute(
            select(Usuario).where(Usuario.nombre_usuario == username)
        ).scalar_one()

        stmt = (
            select(Email).where(Email.usuario_id == user.id)
        )

        result = session.execute(stmt).scalars().fetchall()
        
        return result
    
def crear_grupo(name: str) -> Grupo:
    with Session() as session:
        with session.begin():
            grupo = Grupo(nombre=name)
            session.add(grupo)
            return grupo

def get_group(name: str) -> Grupo | None:
    with Session() as session:
        group = session.execute(
            select(Grupo)
            .where(Grupo.nombre == name)
        ).scalar_one_or_none()

        return group

def create_database():
    Base.metadata.create_all(engine)