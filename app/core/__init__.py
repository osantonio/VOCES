"""
Módulo core - Funcionalidades centrales de la aplicación.

Este módulo centraliza las importaciones de:
- Database: Configuración de base de datos y sesiones
- Seguridad: Funciones de hashing y verificación de contraseñas
- Auditoría: Registro de actividades del sistema
- Templates: Configuración de Jinja2
"""

from app.core.database import get_session, init_db
from app.core.seguridad import hashear_password, verificar_password
from app.core.auditoria import registrar_actividad
from app.core.templates import templates

__all__ = [
    # Database
    "get_session",
    "init_db",
    # Seguridad
    "hashear_password",
    "verificar_password",
    # Auditoría
    "registrar_actividad",
    # Templates
    "templates",
]
