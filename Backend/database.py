from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os # <--- IMPORTANTE

# 1. TRUCO PARA OBTENER SIEMPRE LA RUTA CORRECTA
# Esto busca la carpeta donde está ESTE archivo (database.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Y une esa ruta con el nombre de la base de datos
DB_PATH = os.path.join(BASE_DIR, "habitos_app.db")

# 2. Usamos la ruta absoluta
sqlalchemy_database_url = f"sqlite:///{DB_PATH}"

# 3. Crear el engine
engine = create_engine(
    sqlalchemy_database_url, connect_args={"check_same_thread":False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()