"""
Módulo de seguridad para hasheo de contraseñas y autenticación.
"""

from passlib.context import CryptContext

# Configuración del contexto de hasheo con bcrypt
contexto_password = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashear_password(password: str) -> str:
    """
    Hashea una contraseña usando bcrypt.

    Args:
        password: Contraseña en texto plano

    Returns:
        Hash de la contraseña

    Example:
        >>> hash = hashear_password("MiPassword123")
        >>> print(hash)
        $2b$12$...
    """
    return contexto_password.hash(password)


def verificar_password(password_plano: str, password_hasheado: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su hash.

    Args:
        password_plano: Contraseña en texto plano a verificar
        password_hasheado: Hash de la contraseña almacenado

    Returns:
        True si la contraseña es correcta, False en caso contrario

    Example:
        >>> hash = hashear_password("MiPassword123")
        >>> verificar_password("MiPassword123", hash)
        True
        >>> verificar_password("OtraPassword", hash)
        False
    """
    return contexto_password.verify(password_plano, password_hasheado)
