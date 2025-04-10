from src.db_ops import get_group, crear_grupo, add_users, add_email_to_user, create_database, get_group, get_user, turn_enabled_users, query_users, delete_user, add_email_to_user, get_user_emails
from src.models import Base, Usuario
from src.db import Session, engine
from faker import Faker

fake = Faker(["es_ES", "en_US"])


def main():
    create_database()

    # #grupo_admins = crear_grupo(name="admins")

    # admins = get_group(name="admins")
    # print(admins)    

    # with Session() as session:
    #     usuario = get_user(username="arilopez", session=session)
    #     if usuario is not None and admins is not None:
    #         #print(usuario.emails)

    #         usuario.grupos = [admins]

    #         session.commit()
    #         print(usuario.grupos)
    with Session() as session:
        for _ in range(5):
            usuario = Usuario(nombre_usuario=fake.user_name(), nombre=fake.name())
            session.add(usuario)
        session.commit()

if __name__ == "__main__":
    main()
