from sqlalchemy.orm import Session
import models, schemas
from datetime import date

# --- USUARIOS ---
def seleccionar_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def crear_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = models.Usuario(**usuario.model_dump())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# --- HÁBITOS ---

def seleccionar_habito(db: Session, habito_id: int):
    return db.query(models.Habito).filter(models.Habito.id == habito_id).first()

def seleccionar_habito_por_nombre(db: Session, usuario_id: int, nombre: str):
    #Buscar si un usuario tiene un usuario con ese nombre
    return db.query(models.habito).filter(
        models.Habito.usuario_id == usuario_id, 
        models.Habito.nombre == nombre
    ).first()

def crear_habito(db: Session, habito: schemas.HabitoCreate, usuario_id: int):
    # Convertimos el esquema a diccionario y añadimos el user_id
    db_habito = models.Habito(**habito.model_dump(), usuario_id=usuario_id)
    db.add(db_habito)
    db.commit()
    db.refresh(db_habito)
    return db_habito

def actualizar_habito(db: Session, habito_id: int, habit_actualizacion: schemas.HabitoActualizar):
    # Encontrar el hábito
    db_habito = seleccionar_habito(db, habito_id=habito_id)
    if not db_habito:
        return None
    
    # Extraer los datos correctos del input del usuario
    datos_actualizados = habit_actualizacion.model_dump(exclude_unset=True)

    #Protección para no cambiar el tipo_habito
    if "tipo_habito" in datos_actualizados:
        del datos_actualizados["tipo_habito"]

    # Actualizar manualemente el objeto de la base de datos
    for key, value in datos_actualizados.items():
        setattr(db_habito, key, value)

    # Guardar los cambios
    db.add(db_habito)
    db.commit()
    db.refresh(db_habito)
    return db_habito


def eliminar_habito(db: Session, habito_id: int):
    # Encontrar el hábito
    db_habito = seleccionar_habito(db, habito_id=habito_id)
    if not db_habito:
        return None

    # Eliminarlo y guardar los cambios
    db.delete(db_habito)
    db.commit()
    return db_habito

def seleccionar_habitos_por_usuario(db: Session, usuario_id: int):
    return db.query(models.Habito).filter(models.Habito.usuario_id == usuario_id).all()

# --- ENTRADAS ---
def crear_entrada_habito(db: Session, entrada: schemas.HabitoEntradaCreate, habito_id: int):
    db_entrada = models.HabitoEntrada(
        **entrada.model_dump(), 
        habito_id=habito_id
    )
    db.add(db_entrada)
    db.commit()
    db.refresh(db_entrada)
    return db_entrada

def seleccionar_entrada(db: Session, entrada_id: int):
    return db.query(models.HabitoEntrada).filter(models.HabitoEntrada.id == entrada_id).first()

def seleccionar_entrada_por_fecha(db: Session, habito_id: int, fecha_entrada: date):
    #Busca si ya exite una entrada para ese hábito en esa fecha
    return db.query(models.HabitoEntrada).filter(
        models.HabitoEntrada.habito_id == habito_id,
        models.HabitoEntrada.fecha == fecha_entrada
    ).first()

def actualizar_entrada_habito(db: Session, entrada_id: int, actualizacion_entrada: schemas.HabitoEntradaActualizar):
    db_entrada = seleccionar_entrada(db, entrada_id=entrada_id)
    if not db_entrada:
        return None

    datos_actualizados = actualizacion_entrada.model_dump(exclude_unset=True)

    for key, value in datos_actualizados.items():
        setattr(db_entrada, key, value)

    db.add(db_entrada)
    db.commit()
    db.refresh(db_entrada)
    return db_entrada

def eliminar_entrada_habito(db: Session, entrada_id: int):
    db_entrada = seleccionar_entrada(db, entrada_id=entrada_id)
    if not db_entrada:
        return None

    db.delete(db_entrada)
    db.commit()
    return db_entrada