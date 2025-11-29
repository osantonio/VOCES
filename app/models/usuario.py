from datetime import datetime, timezone
from typing import Optional
from enum import Enum
import random
import string
import re
from sqlmodel import Field, SQLModel
from pydantic import field_validator


# 1. Definición del Mixin de Marcas de Tiempo
class TimestampMixin(SQLModel):
    """
    Mixin para añadir campos de auditoría de fecha de creación y actualización.
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


# 2. Definición del Enum para Roles
class RolUsuario(str, Enum):
    Usuario = "Usuario"
    Editor = "Editor"
    Admin = "Admin"


# 3. Función generadora de UUID personalizado (LLLNNN - estilo matrícula colombiana)
def generar_uuid_personalizado() -> str:
    """
    Genera un UUID personalizado con formato LLLNNN (3 letras + 3 números).
    Ejemplo: ABC123, XYZ789
    """
    letras = "".join(random.choices(string.ascii_uppercase, k=3))
    numeros = "".join(random.choices(string.digits, k=3))
    return f"{letras}{numeros}"


# 4. Definición del Modelo Usuario
class Usuario(TimestampMixin, table=True):
    # Clave primaria: UUID personalizado (LLLNNN)
    id: str = Field(
        primary_key=True,
        default_factory=generar_uuid_personalizado,
        max_length=6,
        nullable=False,
        description="Identificador único con formato LLLNNN (ej: ABC123)",
    )

    # Username ahora es un campo único, no la PK
    username: str = Field(unique=True, index=True, max_length=50, nullable=False)

    email: str = Field(unique=True, index=True, nullable=False)

    # Nota: Este campo almacena el valor de entrada del formulario.
    # EN LA APLICACIÓN, DEBE CONVERTIRSE A HASH ANTES DE PERSISTIRSE
    password: str = Field(
        nullable=False,
        exclude=True,  # Excluye este campo de la mayoría de los esquemas de lectura por seguridad
    )

    nombre: str = Field(max_length=100, nullable=False)
    apellido: str = Field(max_length=100, nullable=False)

    # Soft Delete (Eliminación Suave)
    eliminado_suavemente: bool = Field(default=False, index=True)

    # Campos de perfil y métricas de retención/gamificación
    biografia: Optional[str] = Field(default=None, max_length=500)

    rol: RolUsuario = Field(
        default=RolUsuario.Usuario,
        sa_column_kwargs={"server_default": RolUsuario.Usuario.value},
        index=True,  # Índice para filtrar por rol eficientemente
    )

    puntuacion_reputacion: int = Field(default=0)
    esta_verificado: bool = Field(default=False)

    # Validaciones
    @field_validator("email")
    @classmethod
    def validar_email(cls, valor: str) -> str:
        """
        Valida el formato del email y lo normaliza a minúsculas.
        """
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", valor):
            raise ValueError("Formato de email inválido")
        return valor.lower()

    @field_validator("password")
    @classmethod
    def validar_password(cls, valor: str) -> str:
        """
        Valida que la contraseña tenga al menos 8 caracteres.
        Nota: Este campo debe ser hasheado antes de persistirse en la base de datos.
        """
        if len(valor) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return valor

    @field_validator("username")
    @classmethod
    def validar_username(cls, valor: str) -> str:
        """
        Valida que el username solo contenga caracteres alfanuméricos, guiones y guiones bajos.
        """
        if not re.match(r"^[a-zA-Z0-9_-]+$", valor):
            raise ValueError(
                "El username solo puede contener letras, números, guiones y guiones bajos"
            )
        return valor.lower()
