from src.db_ops import get_user, disable_user, query_users
from src.models import Base
from src.db import engine

def main():
    Base.metadata.create_all(engine)

    usuario = get_user(username="arilopez")
    print(usuario)
    disable_user("arilopez")

    users = query_users()    

    for user in users:
        print(f"nombre_usuario={user.nombre_usuario}, habilitado={user.habilitado}")

if __name__ == "__main__":
    main()
