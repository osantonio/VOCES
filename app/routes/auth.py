"""
Rutas de autenticación (Login, Registro, Logout) con soporte para Jinja2.
"""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, status, Request, Form, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.seguridad import hashear_password, verificar_password
from app.core.auditoria import registrar_actividad
from app.core.templates import templates
from app.models import Usuario, PerfilDemografico, TipoAccion

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.get("/registro", response_class=HTMLResponse)
async def registro_view(request: Request):
    """Renderiza el formulario de registro."""
    return templates.TemplateResponse("auth/registro.html", {"request": request})


@router.post("/registro")
async def registrar_usuario(
    request: Request,
    nombres: Annotated[str, Form()],
    apellidos: Annotated[str, Form()],
    username: Annotated[str, Form()],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: Session = Depends(get_session),
):
    """
    Procesa el formulario de registro.
    """
    # 1. Verificar si el usuario o email ya existen
    statement = select(Usuario).where(
        (Usuario.username == username) | (Usuario.email == email)
    )
    existing_user = session.exec(statement).first()

    if existing_user:
        registrar_actividad(
            session=session,
            tipo_accion=TipoAccion.RegistroExitoso,
            descripcion="Intento de registro fallido: usuario o email ya existe",
            exitoso=False,
            detalles={"username": username, "email": email},
        )
        # Volver a renderizar con error
        return templates.TemplateResponse(
            "auth/registro.html",
            {
                "request": request,
                "error": "El nombre de usuario o correo ya están registrados",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # 2. Crear objeto Usuario
    nuevo_usuario = Usuario(
        nombres=nombres,
        apellidos=apellidos,
        username=username,
        email=email,
        password=hashear_password(password),
    )

    # 3. Guardar en DB
    try:
        session.add(nuevo_usuario)
        session.commit()
        session.refresh(nuevo_usuario)

        # 4. Crear perfil demográfico
        perfil = PerfilDemografico(usuario_id=nuevo_usuario.id)
        session.add(perfil)
        session.commit()

        # 5. Registrar actividad
        registrar_actividad(
            session=session,
            tipo_accion=TipoAccion.RegistroExitoso,
            descripcion="Usuario registrado exitosamente",
            usuario_id=nuevo_usuario.id,
            detalles={"username": username, "email": email},
        )

        # Redirigir al login
        return RedirectResponse(
            url="/auth/login?mensaje=Registro exitoso, por favor inicia sesión",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    except Exception as e:
        session.rollback()
        registrar_actividad(
            session=session,
            tipo_accion=TipoAccion.ErrorSistema,
            descripcion="Error al registrar usuario",
            exitoso=False,
            mensaje_error=str(e),
            detalles={"username": username},
        )
        return templates.TemplateResponse(
            "auth/registro.html",
            {"request": request, "error": f"Error interno: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/login", response_class=HTMLResponse)
async def login_view(request: Request, mensaje: Optional[str] = None):
    """Renderiza el formulario de login."""
    return templates.TemplateResponse(
        "auth/login.html", {"request": request, "mensaje": mensaje}
    )


@router.post("/login")
async def login(
    request: Request,
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
    """
    Procesa el login y establece cookie de sesión.
    """
    # 1. Buscar usuario
    statement = select(Usuario).where(Usuario.username == form_data.username)
    usuario = session.exec(statement).first()

    # 2. Verificar credenciales
    if not usuario or not verificar_password(form_data.password, usuario.password):
        registrar_actividad(
            session=session,
            tipo_accion=TipoAccion.IntentoLoginFallido,
            descripcion="Credenciales inválidas",
            exitoso=False,
            detalles={"username_intentado": form_data.username},
        )
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Usuario o contraseña incorrectos"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # 3. Registrar login exitoso
    registrar_actividad(
        session=session,
        tipo_accion=TipoAccion.Login,
        descripcion="Inicio de sesión exitoso",
        usuario_id=usuario.id,
    )

    # 4. Crear respuesta con redirección y cookie
    # Nota: En un sistema real, aquí generaríamos un JWT
    token = f"fake-jwt-{usuario.username}"

    redirect_url = "/"
    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)

    # Establecer cookie segura
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        max_age=1800,  # 30 minutos
        expires=1800,
    )

    return response


@router.get("/logout")
async def logout(request: Request):
    """Cierra sesión eliminando la cookie."""
    response = RedirectResponse(
        url="/auth/login", status_code=status.HTTP_303_SEE_OTHER
    )
    response.delete_cookie("access_token")
    return response
