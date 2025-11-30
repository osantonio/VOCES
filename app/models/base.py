"""
Mixins base reutilizables para los modelos.
"""

from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


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
