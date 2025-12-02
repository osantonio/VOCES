"""
Utilidades para registrar actividad del usuario en el sistema de auditoría.
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.log_actividad import LogActividad
from app.models.enums import TipoAccion


async def registrar_actividad(
    session: AsyncSession,
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
    await session.commit()
    await session.refresh(log)

    return log


async def obtener_actividad_usuario(
    session: AsyncSession,
    usuario_id: str,
    limite: int = 50,
    tipo_accion: Optional[TipoAccion] = None,
) -> list[LogActividad]:
    """
    Obtiene el historial de actividad de un usuario.
    """
    statement = select(LogActividad).where(LogActividad.usuario_id == usuario_id)

    if tipo_accion:
        statement = statement.where(LogActividad.tipo_accion == tipo_accion)

    statement = statement.order_by(LogActividad.creado_en.desc()).limit(limite)
    result = await session.execute(statement)
    return result.scalars().all()
