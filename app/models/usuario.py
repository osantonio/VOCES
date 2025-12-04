"""
Modelo de Usuario para autenticación y perfil público.
"""

import random
import string
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from pydantic import EmailStr

from app.models.base import TimestampMixin, EstadisticasMixin
from app.models.enums import RolUsuario, EstadoCuenta

if TYPE_CHECKING:
    from app.models.perfil_demografico import PerfilDemografico
    from app.models.redes_sociales import UsuarioRedSocial


def generar_uuid_personalizado() -> str:
    """
    Genera un UUID personalizado con formato LLLNNN (3 letras + 3 números).
    Ejemplo: ABC123, XYZ789
    """
    letras = "".join(random.choices(string.ascii_uppercase, k=3))
    numeros = "".join(random.choices(string.digits, k=3))
    return f"{letras}{numeros}"


class Usuario(TimestampMixin, EstadisticasMixin, table=True):
    """
    Modelo de Usuario para autenticación y perfil público.
    Hereda de TimestampMixin y EstadisticasMixin.
    """

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
        schema_extra={"pattern": r"^[a-zA-Z0-9_-]+$"},
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

    # Relación con perfil demográfico (1:1)
    perfil_demografico: Optional["PerfilDemografico"] = Relationship(
        back_populates="usuario",
        sa_relationship_kwargs={"uselist": False},
    )

    # Relación con redes sociales (1:N)
    redes_sociales: list["UsuarioRedSocial"] = Relationship(
        back_populates="usuario",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
