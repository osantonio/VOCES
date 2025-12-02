"""
Punto de entrada principal de la aplicación VOCES.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.core.database import init_db, async_session_maker
from sqlmodel import select
from app.models import Usuario
from app.routes import auth, main as main_routes, usuarios, logs


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
app.include_router(main_routes.router)
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(logs.router)


@app.middleware("http")
async def inject_current_user(request: Request, call_next):
    """
    Middleware que inyecta `request.state.usuario_actual` para uso en plantillas.
    Deriva el username desde la cookie `access_token` y consulta la base de datos.
    """
    user = None
    token = request.cookies.get("access_token")
    if token and token.startswith("Bearer fake-jwt-"):
        username = token.replace("Bearer fake-jwt-", "")
        try:
            async with async_session_maker() as session:
                result = await session.execute(select(Usuario).where(Usuario.username == username))
                user = result.scalars().first()
        except Exception:
            user = None
    request.state.usuario_actual = user
    response = await call_next(request)
    return response
