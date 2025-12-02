import hashlib
import base64
import bcrypt


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
