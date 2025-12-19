from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas, crud
from validators import validar_entrada_datos 
from datetime import date
from ml_service import entrenar_modelo, predecir_perfil_usuario

router = APIRouter()

# --- USUARIOS  ---

@router.post("/usuarios/", response_model=schemas.Usuario)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.crear_usuario(db=db, usuario=usuario)

@router.get("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def leer_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.seleccionar_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

# --- HÁBITOS  ---

@router.post("/usuarios/{usuario_id}/habitos/", response_model=schemas.Habito)
def crear_habito(usuario_id: int, habito: schemas.HabitoCreate, db: Session = Depends(get_db)):
    # comprobar si el usuario existe ya
    db_usuario = crud.seleccionar_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    habito_existente = crud.seleccionar_habito_por_nombre(db, usuario_id, habito.nombre)
    if habito_existente: 
        raise HTTPException(status_code=400, detail= "Ya tienes un hábito con ese nombre")
    return crud.crear_habito(db=db, habito=habito, usuario_id=usuario_id)

@router.get("/usuarios/{usuario_id}/habitos/", response_model=List[schemas.Habito])
def leer_habitos(usuario_id: int, db: Session = Depends(get_db)):
    return crud.seleccionar_habitos_por_usuario(db, usuario_id=usuario_id)

@router.put("/habitos/{habito_id}", response_model=schemas.Habito)
def actualizar_habito(
    habito_id: int, 
    habito_update: schemas.HabitoActualizar, 
    db: Session = Depends(get_db)
):
    db_habito = crud.actualizar_habito(db, habito_id=habito_id, habit_actualizacion=habito_update)
    if db_habito is None:
        raise HTTPException(status_code=404, detail="Hábito no encontrado")
    return db_habito

@router.delete("/habitos/{habito_id}", response_model=schemas.Habito)
def eliminar_habito(habito_id: int, db: Session = Depends(get_db)):
    db_habito = crud.eliminar_habito(db, habito_id=habito_id)
    if db_habito is None:
        raise HTTPException(status_code=404, detail="Hábito no encontrado")
    return db_habito

# --- ENTRADAS  ---

@router.post("/habitos/{habito_id}/entradas/", response_model=schemas.HabitoEntrada)
def crear_entrada(
    habito_id: int, 
    entrada: schemas.HabitoEntradaCreate, 
    db: Session = Depends(get_db)
):
    # 1. Ir al hábito para comprobar el tipo
    db_habito = crud.seleccionar_habito(db, habito_id=habito_id)
    if not db_habito:
        raise HTTPException(status_code=404, detail="Hábito no encontrado")
    
    # 2. Comprobar frecuencia (duplicados en la misma fecha)
    fecha_a_revisar = entrada.fecha if entrada.fecha else date.today() 
    entrada_existente = crud.seleccionar_entrada_por_fecha(db, habito_id=habito_id)
    if entrada_existente:
        raise HTTPException(status_code=400,
                             detail=f"Ya has registrado una entrada para este hábito en la fecha {fecha_a_revisar}")

    # 3. Validar el JSON
    validar_entrada_datos(db_habito.tipo_habito, entrada.valor)

    # 4. Guardar en DB si pasa la validación
    return crud.crear_entrada_habito(db=db, entrada=entrada, habit_id=habito_id)

@router.get("/entradas/{entrada_id}", response_model=schemas.HabitoEntrada)
def leer_entrada(entrada_id: int, db: Session = Depends(get_db)):
    # Buscamos la entrada específica por ID
    db_entrada = crud.seleccionar_entrada(db, entrada_id=entrada_id)
    
    if db_entrada is None:
        raise HTTPException(status_code=404, detail="Entrada no encontrada")
    
    return db_entrada

@router.put("/entradas/{entrada_id}", response_model=schemas.HabitoEntrada)
def actualizar_entrada(
    entrada_id: int, 
    entrada_update: schemas.HabitoEntradaActualizar, 
    db: Session = Depends(get_db)
):
    # 1. Recuperamos la entrada original para saber de qué TIPO de hábito es
    db_entrada = crud.seleccionar_entrada(db, entrada_id=entrada_id)
    if not db_entrada is None:
        # Nota: db_entrada tiene relación con .habito gracias a models.py
        # Accedemos al tipo del hábito padre (ej: "lectura")
        tipo_habito = db_entrada.habito.tipo_habito
        
        # 2. Si el usuario intenta cambiar el VALOR (el JSON), debemos validarlo de nuevo
        if entrada_update.valor is not None:
            # Usamos tu validador importado
            validar_entrada_datos(tipo_habito, entrada_update.valor)

        # 3. Si todo está bien, actualizamos
        return crud.actualizar_entrada_habito(db=db, entrada_id=entrada_id, actualizacion_entrada=entrada_update)
    
    raise HTTPException(status_code=404, detail="Entrada no encontrada")

@router.delete("/entradas/{entrada_id}", response_model=schemas.HabitoEntrada)
def eliminar_entrada(entrada_id: int, db: Session = Depends(get_db)):
    db_entrada = crud.eliminar_entrada_habito(db, entrada_id=entrada_id)
    if db_entrada is None:
        raise HTTPException(status_code=404, detail="Entrada no encontrada")
    return db_entrada

# --- ML ---

#Endpoint para entrenar el modelo
@router.post("/ml/entrenar", response_model=schemas.MensajeExito)
def entrenar_ia(db: Session = Depends(get_db)):
    try:
        entrenar_modelo(db) # Llamamos a tu función de ml_service.py
        return {"message": "Modelo entrenado y métricas actualizadas correctamente."}
    except Exception as e:
        # Si algo explota (ej. BD vacía), avisamos al frontend
        raise HTTPException(status_code=500, detail=f"Error durante el entrenamiento: {str(e)}")
    
#Enpoint para predecir perfil de usuario
@router.get("/usuarios/{usuario_id}/perfil-ia", response_model=schemas.PerfilIA)
def predecir_perfil(usuario_id: int, db: Session = Depends(get_db)):
    
    # 1. Llamamos a la función
    resultado = predecir_perfil_usuario(db, usuario_id)

    # 2. Gestionamos los posibles errores que devuelve el servicio
    if resultado is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if "error" in resultado:
        # Esto pasa si intentas predecir sin haber entrenado nunca antes
        raise HTTPException(status_code=503, detail="El modelo IA no está entrenado. Ejecuta /ml_service.py primero.")

    # 3. Devolvemos el diccionario (FastAPI lo valida con schemas.PerfilIA)
    return resultado