"""
Modelos para gestión de redes sociales de usuarios.
Permite redes sociales predefinidas (configurables por admin) y personalizadas (por usuario).
"""

from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship

from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.usuario import Usuario


class CatalogoRedSocial(TimestampMixin, table=True):
    """
    Catálogo de tipos de redes sociales predefinidas.
    Configurables por el administrador.
    """

    __tablename__ = "catalogo_red_social"

    id: Optional[int] = Field(default=None, primary_key=True)

    nombre: str = Field(
        max_length=100,
        nullable=False,
        unique=True,
        index=True,
        description="Nombre de la red social (ej: Twitter, Facebook, GitHub)",
    )

    icono_font_awesome: str = Field(
        max_length=100,
        nullable=False,
        description="Clase de Font Awesome (ej: 'fa-brands fa-twitter')",
    )

    url_placeholder: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Placeholder para ayudar al usuario (ej: 'https://twitter.com/tu_usuario')",
    )

    activo: bool = Field(
        default=True,
        nullable=False,
        description="Indica si este tipo de red social está activo",
    )

    # Relación con UsuarioRedSocial
    usuarios_redes: list["UsuarioRedSocial"] = Relationship(
        back_populates="catalogo_red_social"
    )


class UsuarioRedSocial(TimestampMixin, table=True):
    """
    Redes sociales de cada usuario.
    Puede ser una red predefinida (usando tipo_red_social_id)
    o una red personalizada (usando nombre_personalizado e icono_personalizado).
    """

    __tablename__ = "usuario_red_social"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relación con Usuario
    usuario_id: str = Field(
        foreign_key="usuario.id",
        nullable=False,
        index=True,
        description="ID del usuario propietario de esta red social",
    )

    # Relación con CatalogoRedSocial (nullable para redes personalizadas)
    tipo_red_social_id: Optional[int] = Field(
        default=None,
        foreign_key="catalogo_red_social.id",
        nullable=True,
        index=True,
        description="ID del tipo de red social predefinida (NULL si es personalizada)",
    )

    # Campos para redes personalizadas
    nombre_personalizado: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Nombre de la red si es personalizada (ej: 'Mi Blog', 'Portfolio')",
    )

    icono_personalizado: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Código HTML del icono Font Awesome si es personalizada (ej: '<i class=\"fa-brands fa-dev\"></i>')",
    )

    # URL de la red social (obligatorio)
    url: str = Field(
        max_length=500,
        nullable=False,
        description="URL del perfil del usuario en esta red social",
    )

    # Orden de visualización
    orden: int = Field(
        default=0,
        ge=0,
        description="Orden para visualización de redes sociales (menor = primero)",
    )

    # Relaciones
    usuario: "Usuario" = Relationship(back_populates="redes_sociales")
    catalogo_red_social: Optional["CatalogoRedSocial"] = Relationship(
        back_populates="usuarios_redes"
    )
