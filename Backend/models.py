import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, Date, Float, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
from datetime import date, datetime, timezone
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    #Features para entrenar el modelo en clustering
    edad = Column(Integer, nullable=True) 
    genero = Column(String, nullable=True) 
    peso = Column(Float, nullable=True )
    altura = Column(Integer, nullable=True)
    estilo_vida = Column(String, nullable=True)
    nivel_actividad = Column(String, nullable=True)

    timezone = Column(String, nullable=True, default="UTC") 

    
    habitos = relationship("Habito", back_populates="owner")

class Habito(Base):
    __tablename__ = "habitos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    frecuencia = Column(String)  #diariamente, semanalmente...
    
    # Esto define el tipo de dato que esperamos
    
    tipo_habito = Column(String, nullable=False)
    
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    owner = relationship("Usuario", back_populates="habitos")
    entradas = relationship("HabitoEntrada", back_populates="habito")

    #La combinación usuario_id + nombre ha de ser única
    __table_args__ = (
        UniqueConstraint('usuario_id', 'nombre', name='uix_usuario_habito_nombre'),
    )

class HabitoEntrada(Base):
    __tablename__ = "habitos_entradas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, default=date.today)

    creado_a = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    #Esto guarda datos flexibles en un JSON: 
    #Ejemplo para leer {"páginas": 20, "minutes": 30}
    valor = Column(JSON, nullable=True)
    
    habito_id = Column(Integer, ForeignKey("habitos.id"))
    
    habito = relationship("Habito", back_populates="entradas")

    #Para un habito_id no puede repetirse la misma fecha
    __table_args__ = (
        UniqueConstraint('habito_id', 'fecha', name='uix_habito_entrada_fecha'),
    )