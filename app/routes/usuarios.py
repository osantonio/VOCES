# ./app/routes/usuarios.py

"""
Rutas para la gestión de usuarios.
"""

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select
from datetime import datetime

from app.core import templates, get_session
from app.models import Usuario
from app.models.perfil_demografico import PerfilDemografico
from app.models.enums import Sexo

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_class=HTMLResponse)
async def listar_usuarios(
    request: Request, session: AsyncSession = Depends(get_session)
):
    """
    Endpoint que lista todos los usuarios registrados.
    """
    # Consultar todos los usuarios
    statement = select(Usuario).order_by(Usuario.creado_en.desc())
    result = await session.execute(statement)
    usuarios = result.scalars().all()

    return templates.TemplateResponse(
        "usuarios/listar.html", {"request": request, "usuarios": usuarios}
    )


@router.get("/{username}", response_class=HTMLResponse)
async def ver_perfil(
    username: str, request: Request, session: AsyncSession = Depends(get_session)
):
    """
    Endpoint que muestra el perfil completo de un usuario.
    """
    # Consultar usuario con su perfil demográfico
    statement = (
        select(Usuario)
        .where(Usuario.username == username)
        .options(selectinload(Usuario.perfil_demografico))
    )
    result = await session.execute(statement)
    usuario = result.scalars().first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return templates.TemplateResponse(
        "usuarios/perfil.html", {"request": request, "usuario": usuario}
    )


@router.get("/{username}/editar", response_class=HTMLResponse)
async def editar_perfil_form(
    username: str, request: Request, session: AsyncSession = Depends(get_session)
):
    """
    Formulario para editar el perfil de un usuario.
    """
    statement = (
        select(Usuario)
        .where(Usuario.username == username)
        .options(selectinload(Usuario.perfil_demografico))
    )
    result = await session.execute(statement)
    usuario = result.scalars().first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return templates.TemplateResponse(
        "usuarios/editar.html", {"request": request, "usuario": usuario}
    )


@router.post("/{username}/editar", response_class=HTMLResponse)
async def editar_perfil_submit(
    username: str, request: Request, session: AsyncSession = Depends(get_session)
):
    """
    Procesa la actualización del perfil.
    """
    # Obtener usuario
    statement = (
        select(Usuario)
        .where(Usuario.username == username)
        .options(selectinload(Usuario.perfil_demografico))
    )
    result = await session.execute(statement)
    usuario = result.scalars().first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Procesar formulario
    form = await request.form()

    # Actualizar datos básicos de Usuario
    usuario.nombres = form.get("nombres", usuario.nombres)
    usuario.apellidos = form.get("apellidos", usuario.apellidos)
    usuario.biografia = form.get("biografia", usuario.biografia)
    usuario.actualizado_en = datetime.now()

    # Redes sociales
    usuario.twitter_url = form.get("twitter_url") or None
    usuario.facebook_url = form.get("facebook_url") or None
    usuario.instagram_url = form.get("instagram_url") or None
    usuario.linkedin_url = form.get("linkedin_url") or None

    # Actualizar o crear Perfil Demográfico
    if not usuario.perfil_demografico:
        usuario.perfil_demografico = PerfilDemografico(usuario_id=usuario.id)

    perfil = usuario.perfil_demografico

    perfil.telefono = form.get("telefono") or None
    perfil.ciudad = form.get("ciudad") or None
    perfil.departamento = form.get("departamento") or None
    perfil.pais = form.get("pais", "CO")
    perfil.nivel_educativo = form.get("nivel_educativo") or None
    perfil.ocupacion = form.get("ocupacion") or None

    # Sexo (Enum)
    sexo_val = form.get("sexo")
    if sexo_val:
        try:
            perfil.sexo = Sexo(sexo_val)
        except ValueError:
            perfil.sexo = None
    else:
        perfil.sexo = None

    # Fecha Nacimiento
    fecha_nac_str = form.get("fecha_nacimiento")
    if fecha_nac_str:
        try:
            perfil.fecha_nacimiento = datetime.strptime(fecha_nac_str, "%Y-%m-%d")
        except ValueError:
            pass

    session.add(usuario)
    session.add(perfil)
    await session.commit()
    await session.refresh(usuario)

    return RedirectResponse(url=f"/usuarios/{usuario.username}", status_code=303)


@router.post("/{username}/eliminar")
async def eliminar_usuario(
    username: str, request: Request, session: AsyncSession = Depends(get_session)
):
    """
    Endpoint para eliminar un usuario.
    """
    # Buscar el usuario
    statement = select(Usuario).where(Usuario.username == username)
    result = await session.execute(statement)
    usuario = result.scalars().first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Eliminar el usuario (esto también eliminará el perfil demográfico por cascada)
    await session.delete(usuario)
    await session.commit()

    # Redirigir a la lista de usuarios
    return RedirectResponse(url="/usuarios", status_code=303)
