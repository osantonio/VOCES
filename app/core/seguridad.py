import hashlib
import base64
import bcrypt
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def _pre_hash_password(password: str) -> bytes:
    """
    Realiza un pre-hashing de la contraseña usando SHA-256.
    Retorna bytes listos para ser procesados por bcrypt.
    """
    # 1. SHA-256 genera un digest de 32 bytes
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    # 2. Codificamos en base64 para tener caracteres seguros
    return base64.b64encode(digest)


def hashear_password(password: str) -> str:
    """
    Hashea una contraseña usando bcrypt directamente (con pre-hashing SHA-256).
    """
    password_segura = _pre_hash_password(password)
    # Generamos salt y hasheamos
    # bcrypt.hashpw devuelve bytes, decodificamos a str para guardar en DB
    hashed = bcrypt.hashpw(password_segura, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verificar_password(password_plano: str, password_hasheado: str) -> bool:
    """
    Verifica si una contraseña coincide con su hash usando bcrypt.
    """
    try:
        password_segura = _pre_hash_password(password_plano)
        # bcrypt.checkpw espera bytes en ambos argumentos
        return bcrypt.checkpw(password_segura, password_hasheado.encode("utf-8"))
    except Exception:
        return False


def crear_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT firmado.

    Args:
        data: Diccionario con los datos a incluir en el token (típicamente {"sub": username})
        expires_delta: Tiempo de expiración personalizado (opcional)

    Returns:
        Token JWT firmado como string
    """
    to_encode = data.copy()

    # Establecer tiempo de expiración
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # Agregar claims estándar
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})

    # Generar token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verificar_token(token: str) -> Optional[dict]:
    """
    Verifica y decodifica un token JWT.

    Args:
        token: Token JWT a verificar

    Returns:
        Payload del token si es válido, None si es inválido o expirado
    """
    try:
        # Decodificar y verificar token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # Token expirado
        return None
    except jwt.InvalidTokenError:
        # Token inválido (firma incorrecta, formato incorrecto, etc.)
        return None
    except Exception:
        # Cualquier otro error
        return None
