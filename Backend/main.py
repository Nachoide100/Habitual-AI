from fastapi import FastAPI
import models
from database import engine
from routers import router
from fastapi.middleware.cors import CORSMiddleware 

#crea las tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Habit Tracker API",
    description="API para trackear hábitos con validación de ML",
    version="1.0.0"
)


# Configuración de seguridad para permitir que el Frontend hable con el Backend
origins = [
    "http://localhost",
    "http://localhost:3173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # O usa ["*"] para permitir a TODO el mundo (menos seguro)
    allow_credentials=True,
    allow_methods=["*"], # Permitir GET, POST, PUT, DELETE
    allow_headers=["*"],
)

# Connect the routes
app.include_router(router)

@app.get("/")
def read_root():
    return {"status": "Operativo", "message": "Ir a los documentos para ver la API"}



