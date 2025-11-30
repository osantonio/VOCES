"""
Punto de entrada principal de la aplicación VOCES.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Ciclo de vida de la aplicación.
    Se ejecuta al iniciar y detener el servidor.
    """
    # Inicio: Crear tablas si no existen
    await init_db()
    print("✅ Base de datos inicializada")
    yield
    # Fin: Limpieza (si fuera necesaria)


app = FastAPI(
    title="VOCES API",
    description="Plataforma de blog comunitario y reviews",
    version="1.0.0",
    lifespan=lifespan,
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Endpoint raíz para verificar estado"""
    return {"mensaje": "Bienvenido a VOCES API", "estado": "activo", "docs": "/docs"}
