from datetime import datetime, timezone
from typing import Optional
from enum import Enum
import random
import string
from sqlmodel import Field, SQLModel
from pydantic import EmailStr


# 1. Definición del Mixin de Marcas de Tiempo
class TimestampMixin(SQLModel):
    """
    Mixin para añadir campos de auditoría de fecha de creación, actualización y última actividad.
    """

    creado_en: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column_kwargs={
            "server_default": "now()"
        },  # Uso de valor predeterminado del servidor para mayor precisión
    )
    actualizado_en: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column_kwargs={
            "server_default": "now()",
            "onupdate": "now()",
        },  # Actualiza automáticamente en la DB
    )
    ultima_actividad: Optional[datetime] = Field(
        default=None,
        index=True,
        description="Última vez que el usuario realizó una acción en la plataforma",
    )


# 2. Definición de Enums
class RolUsuario(str, Enum):
    """Roles de usuario en la plataforma"""

    Usuario = "Usuario"
    Editor = "Editor"
    Moderador = "Moderador"
    Admin = "Admin"


class EstadoCuenta(str, Enum):
    """Estado de la cuenta del usuario"""

    Activo = "Activo"  # Cuenta activa y verificada
    PendienteVerificacion = "PendienteVerificacion"  # Email no verificado
    Inactivo = "Inactivo"  # Cuenta desactivada por el usuario
    Suspendido = "Suspendido"  # Suspendido temporalmente por moderación
    Baneado = "Baneado"  # Baneado permanentemente
    Eliminado = "Eliminado"  # Soft delete


class Sexo(str, Enum):
    """Sexo del usuario para métricas demográficas"""

    Masculino = "M"
    Femenino = "F"
    Otro = "O"
    PrefieroNoDecir = "N"


# 3. Definición de Mixins Adicionales
class RedesSocialesMixin(SQLModel):
    """Mixin para campos de redes sociales y enlaces externos"""

    sitio_web: Optional[str] = Field(default=None, max_length=255)
    twitter_handle: Optional[str] = Field(
        default=None,
        max_length=50,
        pattern=r"^@?[a-zA-Z0-9_]{1,15}$",
    )


class EstadisticasMixin(SQLModel):
    """Mixin para métricas de gamificación y estadísticas de usuario"""

    puntuacion_reputacion: int = Field(default=0, description="Puntos de reputación")
    total_publicaciones: int = Field(
        default=0, ge=0, description="Total de entradas de blog"
    )
    total_reviews: int = Field(
        default=0, ge=0, description="Total de reviews de restaurantes"
    )
    total_comentarios: int = Field(default=0, ge=0, description="Total de comentarios")
    nivel: int = Field(
        default=1,
        ge=1,
        le=100,
        description="Nivel del usuario basado en actividad",
    )


# 4. Función generadora de UUID personalizado (LLLNNN - estilo matrícula colombiana)
def generar_uuid_personalizado() -> str:
    """
    Genera un UUID personalizado con formato LLLNNN (3 letras + 3 números).
    Ejemplo: ABC123, XYZ789
    """
    letras = "".join(random.choices(string.ascii_uppercase, k=3))
    numeros = "".join(random.choices(string.digits, k=3))
    return f"{letras}{numeros}"


# 5. Definición del Modelo Usuario
class Usuario(TimestampMixin, RedesSocialesMixin, EstadisticasMixin, table=True):
    # Clave primaria: UUID personalizado (LLLNNN)
    id: str = Field(
        primary_key=True,
        default_factory=generar_uuid_personalizado,
        max_length=6,
        nullable=False,
        description="Identificador único con formato LLLNNN (ej: ABC123)",
    )

    # Username ahora es un campo único, no la PK
    # Validación: min 3 caracteres, solo alfanuméricos, guiones y guiones bajos
    username: str = Field(
        unique=True,
        index=True,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_-]+$",
        nullable=False,
    )

    email: EmailStr = Field(unique=True, index=True, max_length=255, nullable=False)

    # Nota: Este campo almacena el valor de entrada del formulario.
    # EN LA APLICACIÓN, DEBE CONVERTIRSE A HASH ANTES DE PERSISTIRSE
    # Validación: mínimo 8 caracteres
    password: str = Field(
        min_length=8,
        nullable=False,
        exclude=True,  # Excluye este campo de la mayoría de los esquemas de lectura por seguridad
    )

    nombres: str = Field(max_length=100, nullable=False)
    apellidos: str = Field(max_length=100, nullable=False)

    # Perfil
    avatar_url: Optional[str] = Field(
        default=None,
        max_length=500,
        description="URL de la imagen de perfil del usuario",
    )
    biografia: Optional[str] = Field(default=None, max_length=500)

    # Datos demográficos (para métricas)
    fecha_nacimiento: Optional[datetime] = Field(
        default=None,
        description="Fecha de nacimiento para estadísticas demográficas",
    )
    sexo: Optional[Sexo] = Field(
        default=None,
        description="Sexo para métricas demográficas",
    )

    # Estado y permisos
    rol: RolUsuario = Field(
        default=RolUsuario.Usuario,
        sa_column_kwargs={"server_default": RolUsuario.Usuario.value},
        index=True,
    )
    estado_cuenta: EstadoCuenta = Field(
        default=EstadoCuenta.PendienteVerificacion,
        sa_column_kwargs={"server_default": EstadoCuenta.PendienteVerificacion.value},
        index=True,
        description="Estado actual de la cuenta del usuario",
    )

    # Token de verificación de email (excluido de esquemas por seguridad)
    token_verificacion_email: Optional[str] = Field(
        default=None,
        exclude=True,
        max_length=255,
    )
