import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import date, datetime
from enum import Enum

# Enumeraciones para las distintas categorías (evitar datos repetidos escritos diferente)
class CategoriaLibro(str, Enum):
    FICCION = "ficcion"
    NO_FICCION = "no_ficcion"
    DESARROLLO = "desarrollo"
    TERROR = "terror"
    ROMANTICO = "romantico"
    HISTORICO = "historico"
    OTRO = "otro"

class MomentoDia(str, Enum):
    MANANA = "mañana"
    TARDE = "tarde"
    NOCHE = "noche"

class TipoSocial(str, Enum):
    FAMILIA = "familia"
    AMIGOS = "amigos"
    COMPAÑEROS_TRABAJO = "compañeros de trabajo"

class TipoOcio(str, Enum):
    JUEGOMESA = "juego de mesa"
    VIDEOJUEGOS = "videojuegos"
    TELEVISION = "ver la televisión"
    DIBUJO_ARTE = "hobbies artísiticos"


# --- VALORES PARA HÁBITOS ESPECÍFICOS ---
#Determinamos los diferentes tipos de hábitos y ponemos reglas para sus valores
class LecturaValor(BaseModel):
    paginas: int = Field(ge=0)
    minutos: int = Field(ge=0)
    categoria: CategoriaLibro 

class FitnessValor(BaseModel):
    duracion_minutos: int = Field(gt=0)
    distancia_km: Optional[float] = 0.0
    intensidad: int = Field(ge=0, le=5)
    tipo_ejercicio: Optional[str] = "cardio" #ej. "pesas", "yoga"
    

class SuenoValor(BaseModel):
    horas: float = Field(ge=0, le=24)
    calidad: int = Field(ge=1, le=10, description="1 (Horrible) - 10 (Perfecto)")
    madrugar: bool

class NutricionValor(BaseModel):
    agua_litros: float = Field(ge=0)
    cheat_meal: bool
    fruta: int #he comido 3 o más unidades de fruta
    verdura: int
    proteina_animal: int
    hidratos: int

class MeditacionValor(BaseModel):
    minutos: int
    momento: MomentoDia
    estres_antes: int = Field(ge=1, le=10)
    estres_despues: int = Field(ge=1, le=10)

class EstadoAnimoValor(BaseModel):
    puntuacion_dia: int = Field(ge=1, le=10)
    nivel_energia: int = Field(ge=1, le=10)
    notas: Optional[str] = None

class SocialValor(BaseModel):
    minutos: int
    momento: MomentoDia
    tipo_social: TipoSocial

class HabitoNoSaludableValor(BaseModel):
    tabaco: int
    alcohol: int
    sedentarismo: int #horas sentado

class OcioValor(BaseModel):
    minutos: int
    momento: MomentoDia
    tipo_ocio: TipoOcio




# --- SCHEMAS BASE ---

class HabitoEntradaBase(BaseModel):
    fecha: Optional[date] = None #si es missing usaremos la fecha de hoy
    valor: Dict[str, Any] 

class HabitoEntradaCreate(HabitoEntradaBase):
    pass

class HabitoEntradaActualizar(BaseModel):
    fecha: Optional[date] = None
    valor: Optional[Dict[str, Any]] = None

class HabitoEntrada(HabitoEntradaBase):
    id: int
    habito_id: int
    create_a: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class HabitoBase(BaseModel):
    nombre: str
    frecuencia: str
    tipo_habito: str 

class HabitoCreate(HabitoBase):
    pass

class HabitoActualizar(BaseModel): 
    nombre: Optional[str] = None
    frecuencia: Optional[str] = None
    #no daremos opción de cambiar el tipo de hábito

class Habito(HabitoBase):
    id: int
    usuario_id: int
    entradas: List[HabitoEntrada] = []
    model_config = ConfigDict(from_attributes=True)

class UsuarioBase(BaseModel):
    nombre: str
    edad: Optional[int] = None
    genero: Optional[str] = None
    peso: Optional[float] = None
    altura: Optional[int] = None
    estilo_vida: Optional[str] = None
    nivel_actividad: Optional[str] = None
    timezone: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id: int
    habitos: List[Habito] = []
    model_config = ConfigDict(from_attributes=True)

# -- MODELOS ---
class PerfilIA(BaseModel):
    grupo_id: int
    perfil_ia: str
    recomendacion: str
    metricas: Dict[str, float] # Devuelve las métricas individuales del usuario

class MensajeExito(BaseModel):
        message: str