"""
Modelo de Perfil Demográfico para encuestas y estadísticas.
Extensión 1:1 de Usuario - no necesita timestamps propios.
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

from app.models.enums import Sexo

if TYPE_CHECKING:
    from app.models.usuario import Usuario


class PerfilDemografico(SQLModel, table=True):
    """
    Perfil demográfico del usuario para encuestas y estadísticas.
    Relación 1:1 con Usuario. El usuario decide si completa estos datos.
    """

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relación con Usuario (1:1)
    usuario_id: str = Field(
        foreign_key="usuario.id",
        unique=True,
        index=True,
        description="ID del usuario asociado",
    )
    usuario: Optional["Usuario"] = Relationship(back_populates="perfil_demografico")

    # Datos demográficos
    fecha_nacimiento: Optional[datetime] = Field(
        default=None,
        description="Fecha de nacimiento para estadísticas demográficas",
    )
    sexo: Optional[Sexo] = Field(
        default=None,
        description="Sexo para métricas demográficas",
    )

    # Datos de contacto
    telefono: Optional[str] = Field(
        default=None,
        max_length=20,
        schema_extra={"pattern": r"^\+?[0-9\s\-\(\)]+$"},
        description="Número de teléfono de contacto",
    )

    # Ubicación geográfica
    ciudad: Optional[str] = Field(
        default=None,
        max_length=100,
        index=True,
        description="Ciudad de residencia",
    )
    departamento: Optional[str] = Field(
        default=None,
        max_length=100,
        index=True,
        description="Departamento/Estado de residencia",
    )
    pais: str = Field(
        default="CO",
        max_length=2,
        description="Código ISO del país (por defecto Colombia)",
    )

    # Datos socioeconómicos (para encuestas)
    nivel_educativo: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Nivel educativo alcanzado",
    )
    ocupacion: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Ocupación actual",
    )
