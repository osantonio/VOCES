"""
Utilidades para registrar actividad del usuario en el sistema de auditoría.
"""

from typing import Optional
from sqlmodel import Session

from app.models.log_actividad import LogActividad
from app.models.enums import TipoAccion


def registrar_actividad(
    session: Session,
    tipo_accion: TipoAccion,
    descripcion: str,
    usuario_id: Optional[str] = None,
    detalles: Optional[dict] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    exitoso: bool = True,
    mensaje_error: Optional[str] = None,
) -> LogActividad:
    """
    Registra una actividad del usuario en el sistema de auditoría.

    Args:
        session: Sesión de SQLModel
        tipo_accion: Tipo de acción (enum TipoAccion)
        descripcion: Descripción legible de la acción
        usuario_id: ID del usuario (opcional para acciones anónimas)
        detalles: Datos adicionales en formato dict
        ip_address: IP desde donde se realizó la acción
        user_agent: User agent del navegador
        exitoso: Si la acción fue exitosa
        mensaje_error: Mensaje de error si falló

    Returns:
        LogActividad creado

    Example:
        >>> registrar_actividad(
        ...     session=session,
        ...     tipo_accion=TipoAccion.Login,
        ...     descripcion="Usuario inició sesión exitosamente",
        ...     usuario_id="ABC123",
        ...     ip_address="192.168.1.1",
        ...     detalles={"navegador": "Chrome"}
        ... )
    """
    log = LogActividad(
        usuario_id=usuario_id,
        tipo_accion=tipo_accion,
        descripcion=descripcion,
        detalles=detalles,
        ip_address=ip_address,
        user_agent=user_agent,
        exitoso=exitoso,
        mensaje_error=mensaje_error,
    )

    session.add(log)
    session.commit()
    session.refresh(log)

    return log


def obtener_actividad_usuario(
    session: Session,
    usuario_id: str,
    limite: int = 50,
    tipo_accion: Optional[TipoAccion] = None,
) -> list[LogActividad]:
    """
    Obtiene el historial de actividad de un usuario.

    Args:
        session: Sesión de SQLModel
        usuario_id: ID del usuario
        limite: Número máximo de registros a devolver
        tipo_accion: Filtrar por tipo de acción específico

    Returns:
        Lista de LogActividad ordenados por fecha (más reciente primero)
    """
    query = session.query(LogActividad).filter(LogActividad.usuario_id == usuario_id)

    if tipo_accion:
        query = query.filter(LogActividad.tipo_accion == tipo_accion)

    return query.order_by(LogActividad.creado_en.desc()).limit(limite).all()
