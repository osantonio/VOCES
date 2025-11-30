"""
Enumeraciones para los modelos de la aplicación.
"""

from enum import Enum


class RolUsuario(str, Enum):
    """Roles de usuario en la plataforma"""

    Usuario = "Usuario"
    Editor = "Editor"
    Moderador = "Moderador"
    Admin = "Admin"


class EstadoCuenta(str, Enum):
    """Estado de la cuenta del usuario"""

    Activo = "Activo"  # Cuenta activa y verificada
    PendienteVerificacion = "PendienteVerificacion"  # Email no verificado
    Inactivo = "Inactivo"  # Cuenta desactivada por el usuario
    Suspendido = "Suspendido"  # Suspendido temporalmente por moderación
    Baneado = "Baneado"  # Baneado permanentemente
    Eliminado = "Eliminado"  # Soft delete


class Sexo(str, Enum):
    """Sexo del usuario para métricas demográficas"""

    Masculino = "M"
    Femenino = "F"
    Otro = "O"
    PrefieroNoDecir = "N"


class TipoAccion(str, Enum):
    """Tipos de acciones del usuario para auditoría y logs"""

    # Autenticación
    Login = "Login"
    Logout = "Logout"
    RegistroExitoso = "RegistroExitoso"
    IntentoLoginFallido = "IntentoLoginFallido"

    # Perfil
    ActualizacionPerfil = "ActualizacionPerfil"
    CambioPassword = "CambioPassword"
    VerificacionEmail = "VerificacionEmail"

    # Contenido
    CreacionPublicacion = "CreacionPublicacion"
    EdicionPublicacion = "EdicionPublicacion"
    EliminacionPublicacion = "EliminacionPublicacion"
    CreacionReview = "CreacionReview"
    EdicionReview = "EdicionReview"
    EliminacionReview = "EliminacionReview"
    CreacionComentario = "CreacionComentario"
    EliminacionComentario = "EliminacionComentario"

    # Interacciones
    Like = "Like"
    Unlike = "Unlike"
    Compartir = "Compartir"
    Seguir = "Seguir"
    DejarSeguir = "DejarSeguir"

    # Encuestas
    RespuestaEncuesta = "RespuestaEncuesta"

    # Moderación
    ReporteContenido = "ReporteContenido"
    AccionModeracion = "AccionModeracion"

    # Sistema
    ErrorSistema = "ErrorSistema"
    AccesoNoAutorizado = "AccesoNoAutorizado"
