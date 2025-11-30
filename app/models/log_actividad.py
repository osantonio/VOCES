"""
Modelo de Auditoría para registrar todas las acciones del usuario.
"""

from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel, Column, JSON

from app.models.enums import TipoAccion


class LogActividad(SQLModel, table=True):
    """
    Registro de auditoría de todas las acciones del usuario.
    Funciona como un log de consola para análisis, debugging y seguridad.
    """

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relación con Usuario
    usuario_id: Optional[str] = Field(
        default=None,
        foreign_key="usuario.id",
        index=True,
        description="ID del usuario que realizó la acción (null para acciones anónimas)",
    )

    # Tipo de acción
    tipo_accion: TipoAccion = Field(
        index=True,
        description="Tipo de acción realizada",
    )

    # Descripción de la acción
    descripcion: str = Field(
        max_length=500,
        description="Descripción legible de la acción",
    )

    # Datos adicionales en formato JSON
    metadata: Optional[dict] = Field(
        default=None,
        sa_column=Column(JSON),
        description="Datos adicionales de la acción en formato JSON",
    )

    # Información de contexto
    ip_address: Optional[str] = Field(
        default=None,
        max_length=45,  # IPv6 puede ser hasta 45 caracteres
        description="Dirección IP desde donde se realizó la acción",
    )

    user_agent: Optional[str] = Field(
        default=None,
        max_length=500,
        description="User agent del navegador/cliente",
    )

    # Información de éxito/error
    exitoso: bool = Field(
        default=True,
        index=True,
        description="Si la acción fue exitosa o falló",
    )

    mensaje_error: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Mensaje de error si la acción falló",
    )

    # Timestamp
    creado_en: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
        description="Momento exacto en que ocurrió la acción",
    )

    # Relación con Usuario (opcional para poder hacer queries)
    # usuario: Optional["Usuario"] = Relationship(back_populates="logs_actividad")
