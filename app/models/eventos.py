"""
Eventos de SQLAlchemy para mantener sincronizados los timestamps.
"""

from datetime import datetime, timezone
from sqlalchemy import event
from app.models.perfil_demografico import PerfilDemografico


@event.listens_for(PerfilDemografico, "before_update")
def actualizar_timestamp_usuario(mapper, connection, target):
    """
    Cuando se actualiza el PerfilDemografico, también actualizar
    el timestamp del Usuario relacionado.

    Esto mantiene usuario.actualizado_en sincronizado con cualquier
    cambio en los datos del usuario, incluyendo su perfil demográfico.
    """
    if target.usuario:
        target.usuario.actualizado_en = datetime.now(timezone.utc)


@event.listens_for(PerfilDemografico, "after_insert")
def actualizar_timestamp_usuario_insert(mapper, connection, target):
    """
    Cuando se crea un PerfilDemografico, actualizar el timestamp del Usuario.
    """
    if target.usuario:
        target.usuario.actualizado_en = datetime.now(timezone.utc)
