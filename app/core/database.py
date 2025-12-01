"""
Configuración de la base de datos con soporte para PgBouncer.

Usa asyncpg para conexiones asíncronas y NullPool para delegar
el manejo de conexiones a PgBouncer.
"""

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager  # noqa: F401

from dotenv import load_dotenv
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# Importar modelos para que SQLModel los detecte al crear tablas
from app.models import *  # noqa: F401, F403

load_dotenv()

# Obtener URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada en el archivo .env")

# Asegurar que usamos el driver asíncrono
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Configuración del motor de base de datos
# poolclass=NullPool es CRÍTICO para usar con PgBouncer
# Esto evita que SQLAlchemy mantenga conexiones inactivas que podrían
# entrar en conflicto con el pool de PgBouncer.
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Log de consultas SQL (desactivar en producción)
    poolclass=NullPool,
    future=True,  # future se en
)

# Factory de sesiones asíncronas
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependencia para obtener una sesión de base de datos en los endpoints.
    """
    async with async_session_maker() as session:
        yield session


async def init_db():
    """
    Inicializa la base de datos creando las tablas definidas en los modelos.
    """
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all) # Descomentar para reiniciar DB
        await conn.run_sync(SQLModel.metadata.create_all)
