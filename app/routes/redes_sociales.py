"""
Rutas para gestión de redes sociales de usuarios.
"""

from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import select

from app.core.database import async_session_maker
from app.core import templates
from app.models import CatalogoRedSocial, UsuarioRedSocial

router = APIRouter(prefix="/redes", tags=["redes"])


@router.get("/", response_class=HTMLResponse)
async def listar_mis_redes(request: Request):
    """Listar las redes sociales del usuario actual."""
    usuario_actual = request.state.usuario_actual
    if not usuario_actual:
        return RedirectResponse(
            url="/auth/login", status_code=status.HTTP_303_SEE_OTHER
        )

    async with async_session_maker() as session:
        # Obtener tipos de redes sociales activos
        result_tipos = await session.execute(
            select(CatalogoRedSocial)
            .where(CatalogoRedSocial.activo)
            .order_by(CatalogoRedSocial.nombre)
        )
        tipos_disponibles = result_tipos.scalars().all()

        # Obtener redes sociales del usuario
        result_redes = await session.execute(
            select(UsuarioRedSocial)
            .where(UsuarioRedSocial.usuario_id == usuario_actual.id)
            .order_by(UsuarioRedSocial.orden)
        )
        mis_redes = result_redes.scalars().all()

    return templates.TemplateResponse(
        "redes_sociales/listar.html",
        {
            "request": request,
            "tipos_disponibles": tipos_disponibles,
            "mis_redes": mis_redes,
        },
    )


@router.get("/crear", response_class=HTMLResponse)
async def crear_red_form(request: Request):
    """Mostrar formulario para agregar nueva red social."""
    usuario_actual = request.state.usuario_actual
    if not usuario_actual:
        return RedirectResponse(
            url="/auth/login", status_code=status.HTTP_303_SEE_OTHER
        )

    async with async_session_maker() as session:
        # Obtener tipos de redes sociales activos
        result_tipos = await session.execute(
            select(CatalogoRedSocial)
            .where(CatalogoRedSocial.activo)
            .order_by(CatalogoRedSocial.nombre)
        )
        tipos_disponibles = result_tipos.scalars().all()

    return templates.TemplateResponse(
        "redes_sociales/crear.html",
        {
            "request": request,
            "tipos_disponibles": tipos_disponibles,
        },
    )


@router.post("/agregar-predefinida")
async def agregar_red_predefinida(
    request: Request,
    tipo_red_social_id: int = Form(...),
    url: str = Form(...),
):
    """Agregar una red social predefinida al perfil del usuario."""
    usuario_actual = request.state.usuario_actual
    if not usuario_actual:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    async with async_session_maker() as session:
        # Verificar que el tipo existe y está activo
        result_tipo = await session.execute(
            select(CatalogoRedSocial).where(
                CatalogoRedSocial.id == tipo_red_social_id, CatalogoRedSocial.activo
            )
        )
        tipo = result_tipo.scalars().first()
        if not tipo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de red social no encontrado",
            )

        # Verificar que el usuario no tenga ya esta red
        result_existente = await session.execute(
            select(UsuarioRedSocial).where(
                UsuarioRedSocial.usuario_id == usuario_actual.id,
                UsuarioRedSocial.tipo_red_social_id == tipo_red_social_id,
            )
        )
        existente = result_existente.scalars().first()
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya tienes esta red social agregada",
            )

        # Obtener el siguiente orden
        result_max_orden = await session.execute(
            select(UsuarioRedSocial.orden)
            .where(UsuarioRedSocial.usuario_id == usuario_actual.id)
            .order_by(UsuarioRedSocial.orden.desc())
        )
        max_orden = result_max_orden.scalars().first()
        nuevo_orden = (max_orden + 1) if max_orden is not None else 0

        # Crear la red social
        nueva_red = UsuarioRedSocial(
            usuario_id=usuario_actual.id,
            tipo_red_social_id=tipo_red_social_id,
            url=url,
            orden=nuevo_orden,
        )
        session.add(nueva_red)
        await session.commit()

    return RedirectResponse(url="/redes", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/crear")
async def agregar_red_personalizada(
    request: Request,
    nombre: str = Form(...),
    icono: str = Form(...),
    url: str = Form(...),
):
    """Agregar una red social personalizada al perfil del usuario."""
    usuario_actual = request.state.usuario_actual
    if not usuario_actual:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    async with async_session_maker() as session:
        # Obtener el siguiente orden
        result_max_orden = await session.execute(
            select(UsuarioRedSocial.orden)
            .where(UsuarioRedSocial.usuario_id == usuario_actual.id)
            .order_by(UsuarioRedSocial.orden.desc())
        )
        max_orden = result_max_orden.scalars().first()
        nuevo_orden = (max_orden + 1) if max_orden is not None else 0

        # Crear la red social personalizada
        nueva_red = UsuarioRedSocial(
            usuario_id=usuario_actual.id,
            tipo_red_social_id=None,  # NULL = personalizada
            nombre_personalizado=nombre,
            icono_personalizado=icono,
            url=url,
            orden=nuevo_orden,
        )
        session.add(nueva_red)
        await session.commit()

    return RedirectResponse(url="/redes", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/eliminar/{red_id}")
async def eliminar_red_social(request: Request, red_id: int):
    """Eliminar una red social del perfil del usuario."""
    usuario_actual = request.state.usuario_actual
    if not usuario_actual:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    async with async_session_maker() as session:
        # Buscar la red social
        result = await session.execute(
            select(UsuarioRedSocial).where(
                UsuarioRedSocial.id == red_id,
                UsuarioRedSocial.usuario_id == usuario_actual.id,
            )
        )
        red = result.scalars().first()
        if not red:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Red social no encontrada"
            )

        # Eliminar
        await session.delete(red)
        await session.commit()

    return RedirectResponse(url="/redes", status_code=status.HTTP_303_SEE_OTHER)
