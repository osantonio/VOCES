"""
Punto de entrada principal de la aplicación VOCES.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.database import init_db
from app.routes import auth


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

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Registrar rutas
app.include_router(auth.router)


@app.get("/")
async def root():
    """Endpoint raíz para verificar estado"""
    return {"mensaje": "Bienvenido a VOCES API", "estado": "activo", "docs": "/docs"}
