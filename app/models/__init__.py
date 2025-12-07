"""
Modelos de la aplicación VOCES.

Este paquete contiene todos los modelos de base de datos:
- Usuario: Autenticación y perfil público
- PerfilDemografico: Datos demográficos para encuestas
- LogActividad: Auditoría y registro de acciones
- Enums: RolUsuario, EstadoCuenta, Sexo, TipoAccion
- Mixins: TimestampMixin, EstadisticasMixin
"""

# Importar enums
from app.models.enums import RolUsuario, EstadoCuenta, Sexo, TipoAccion

# Importar mixins
from app.models.base import TimestampMixin, EstadisticasMixin

# Importar modelos
from app.models.usuario import Usuario, generar_uuid_personalizado
from app.models.perfil_demografico import PerfilDemografico
from app.models.log_actividad import LogActividad
# Redes sociales eliminadas del proyecto

# Importar eventos (esto registra los listeners automáticamente)
from app.models import eventos  # noqa: F401

__all__ = [
    # Enums
    "RolUsuario",
    "EstadoCuenta",
    "Sexo",
    "TipoAccion",
    # Mixins
    "TimestampMixin",
    "EstadisticasMixin",
    # Modelos
    "Usuario",
    "PerfilDemografico",
    "LogActividad",
    # Utilidades
    "generar_uuid_personalizado",
]
