from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#1. Definir el URL de la base de datos
sqlalchemy_database_url = "sqlite:///./habitos_app.db"

#2. Crear el engine
engine = create_engine(
    sqlalchemy_database_url, connect_args={"check_same_thread":False}
)

#3. Crear la sesión local
SessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False, 
                            bind=engine)


#4. Crear la clase Base (de la que heredaran nuestros modelos)
Base = declarative_base()

#5.  Función para conectar con la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()