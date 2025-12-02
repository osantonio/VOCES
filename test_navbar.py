"""
Pruebas unitarias para la lógica del componente Navbar.

Se valida la generación de iniciales para el avatar y casos límite.
"""

from types import SimpleNamespace
from app.core.templates import user_initials


def test_iniciales_nombres_apellidos():
    user = SimpleNamespace(nombres="Juan Carlos", apellidos="Pérez Gómez", username="juan")
    ini = user_initials(user)
    assert ini == "JP", f"Iniciales esperadas 'JP', obtenido '{ini}'"


def test_iniciales_solo_username():
    user = SimpleNamespace(nombres=None, apellidos=None, username="maria")
    ini = user_initials(user)
    assert ini == "MA", f"Iniciales esperadas 'MA', obtenido '{ini}'"


def test_iniciales_campos_vacios():
    user = SimpleNamespace(nombres="", apellidos="", username="")
    ini = user_initials(user)
    assert ini == "?", f"Iniciales esperadas '?', obtenido '{ini}'"


if __name__ == "__main__":
    # Ejecutar pruebas de manera simple
    test_iniciales_nombres_apellidos()
    test_iniciales_solo_username()
    test_iniciales_campos_vacios()
    print("✓ Pruebas de Navbar ejecutadas correctamente")

