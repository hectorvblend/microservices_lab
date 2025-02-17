from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base

from src.settings import (
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    DB_PORT
    )

# Configura la cadena de conexión (reemplaza los valores con los tuyos)
DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{DB_PORT}/{POSTGRES_DB}'

# Crea una instancia del motor SQLAlchemy
ENGINE = create_engine(DATABASE_URL)

# Crea una sesión
SESSION = sessionmaker(bind=ENGINE)
session = SESSION()
BASE = declarative_base()

def excecute(stmt,engine=ENGINE):
    with engine.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()
        return result

# Test database health:
def db_health():
    try:
        ENGINE = create_engine(DATABASE_URL)
        connection = ENGINE.connect()
        print("Database connection successful")
        connection.close()
    except OperationalError as e:
        print("Error to connect database:", e)
