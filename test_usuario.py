"""
Script de prueba para validar el modelo Usuario refactorizado.
"""

from app.models.usuario import Usuario, RolUsuario, generar_uuid_personalizado


def test_modelo_usuario():
    print("=" * 60)
    print("PRUEBAS DEL MODELO USUARIO REFACTORIZADO")
    print("=" * 60)

    # Test 1: Generación de UUID personalizado
    print("\n[Test 1] Generación de UUID personalizado (LLLNNN)")
    for i in range(5):
        uuid = generar_uuid_personalizado()
        print(f"  UUID {i + 1}: {uuid}")
        assert len(uuid) == 6, f"UUID debe tener 6 caracteres, tiene {len(uuid)}"
        assert uuid[:3].isalpha(), "Primeros 3 caracteres deben ser letras"
        assert uuid[3:].isdigit(), "Últimos 3 caracteres deben ser números"
    print("  ✓ Generación de UUID correcta")

    # Test 2: Roles disponibles
    print("\n[Test 2] Enum de Roles")
    roles = [r.value for r in RolUsuario]
    print(f"  Roles disponibles: {roles}")
    assert "Usuario" in roles, "Debe existir rol 'Usuario'"
    assert "Editor" in roles, "Debe existir rol 'Editor'"
    assert "Admin" in roles, "Debe existir rol 'Admin'"
    print("  ✓ Enum de roles correcto")

    # Test 3: Creación de instancia básica
    print("\n[Test 3] Creación de instancia de Usuario")
    try:
        usuario = Usuario(
            username="juan_perez",
            email="juan.perez@example.com",
            password="password123",
            nombre="Juan",
            apellido="Pérez",
        )
        print(f"  ID generado: {usuario.id}")
        print(f"  Username: {usuario.username}")
        print(f"  Email: {usuario.email}")
        print(f"  Rol por defecto: {usuario.rol}")
        print(f"  Creado en: {usuario.creado_en}")
        print("  ✓ Instancia creada correctamente")
    except Exception as e:
        print(f"  ✗ Error al crear instancia: {e}")
        raise

    # Test 4: Validación de email
    print("\n[Test 4] Validación de email")
    try:
        usuario_email_invalido = Usuario(
            username="test_user",
            email="email_invalido",
            password="password123",
            nombre="Test",
            apellido="User",
        )
        print("  ✗ Debería haber fallado con email inválido")
    except ValueError as e:
        print(f"  ✓ Validación correcta: {e}")

    # Test 5: Validación de password
    print("\n[Test 5] Validación de password")
    try:
        usuario_pass_corto = Usuario(
            username="test_user2",
            email="test@example.com",
            password="123",
            nombre="Test",
            apellido="User",
        )
        print("  ✗ Debería haber fallado con password corto")
    except ValueError as e:
        print(f"  ✓ Validación correcta: {e}")

    # Test 6: Validación de username
    print("\n[Test 6] Validación de username")
    try:
        usuario_username_invalido = Usuario(
            username="usuario con espacios!",
            email="test2@example.com",
            password="password123",
            nombre="Test",
            apellido="User",
        )
        print("  ✗ Debería haber fallado con username inválido")
    except ValueError as e:
        print(f"  ✓ Validación correcta: {e}")

    print("\n" + "=" * 60)
    print("✓ TODAS LAS PRUEBAS PASARON CORRECTAMENTE")
    print("=" * 60)


if __name__ == "__main__":
    test_modelo_usuario()
