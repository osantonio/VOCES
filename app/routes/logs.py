"""
Rutas para la gestión y visualización de logs de actividad.
"""

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload

from app.core import templates, get_session
from app.models import LogActividad, Usuario

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("/", response_class=HTMLResponse)
async def listar_logs(request: Request, session: AsyncSession = Depends(get_session)):
    """
    Endpoint que lista los logs de actividad recientes.
    """
    # Consultar logs ordenados por fecha descendente
    # Cargamos la relación con usuario para mostrar quién hizo la acción
    statement = (
        select(LogActividad, Usuario)
        .outerjoin(Usuario, LogActividad.usuario_id == Usuario.id)
        .order_by(LogActividad.creado_en.desc())
        .limit(50)
    )

    result = await session.execute(statement)
    logs_con_usuario = result.all()  # Retorna lista de tuplas (LogActividad, Usuario)

    return templates.TemplateResponse(
        "auditoria/listar.html", {"request": request, "logs": logs_con_usuario}
    )


@router.get("/{log_id}", response_class=HTMLResponse)
async def ver_log(
    log_id: int, request: Request, session: AsyncSession = Depends(get_session)
):
    """
    Endpoint que muestra el detalle de un log específico.
    """
    statement = (
        select(LogActividad, Usuario)
        .outerjoin(Usuario, LogActividad.usuario_id == Usuario.id)
        .where(LogActividad.id == log_id)
    )
    result = await session.execute(statement)
    log_data = result.first()

    if not log_data:
        raise HTTPException(status_code=404, detail="Log no encontrado")

    log, usuario = log_data

    return templates.TemplateResponse(
        "auditoria/ver.html", {"request": request, "log": log, "usuario": usuario}
    )
