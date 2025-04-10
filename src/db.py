from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# psycopg2 es el conector de bases de datos por defecto para postgres.
engine = create_engine("postgresql+psycopg:///test_db_2025", echo=False)
Session = sessionmaker(engine) 