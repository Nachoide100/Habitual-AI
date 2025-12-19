from fastapi import HTTPException
from pydantic import ValidationError
from typing import Dict, Any

# Importamos todos los hábitos específicos del fichero schemas.py
from schemas import (
    LecturaValor,
    FitnessValor,
    SuenoValor,
    NutricionValor,
    MeditacionValor,
    EstadoAnimoValor, 
    SocialValor,  
    HabitoNoSaludableValor,
    OcioValor
)

def validar_entrada_datos(tipo_habito: str, data: Dict[str, Any]):
    # Si no hay datos, lanzamos error inmediatamente
    if not data:
        raise HTTPException(status_code=400, detail="Se requieren detalles para completar este hábito.")

    try:
        # Lógica de despacho: Según el tipo, validamos con su esquema
        if tipo_habito == "lectura":
            # Esto verificará páginas, minutos y que la categoría sea válida
            LecturaValor(**data)
            
        elif tipo_habito == "fitness":
            FitnessValor(**data)
            
        elif tipo_habito == "sueno":
            SuenoValor(**data)
            
        elif tipo_habito == "nutricion":
            NutricionValor(**data)
            
        elif tipo_habito == "meditacion":
            MeditacionValor(**data)
            
        elif tipo_habito == "estado_animo":
            EstadoAnimoValor(**data)
        
        elif tipo_habito == "actividad_social":
            SocialValor(**data)
       
        elif tipo_habito == "habito_saludable":
            HabitoNoSaludableValor(**data)
        
        elif tipo_habito == "actividad_ocio":
            OcioValor(**data)
        
        else:
            # Si el tipo de hábito es genérico (ej. "check"), permitimos cualquier cosa o nada
            pass

    except ValidationError as e:
        # Pydantic nos da errores muy detallados, se los pasamos al frontend
        # Ejemplo de error: "campo 'paginas' debe ser mayor que 0"
        errores = e.errors()
        mensaje_limpio = f"Error en los datos de {tipo_habito}: {errores[0]['msg']} en campo '{errores[0]['loc']}'"
        raise HTTPException(status_code=422, detail=mensaje_limpio)
        
    except ValueError as e:
        # Captura errores de Enums (ej. enviar "Ficcion" cuando solo aceptamos "ficcion")
        raise HTTPException(status_code=422, detail=f"Valor inválido: {str(e)}")

    return True