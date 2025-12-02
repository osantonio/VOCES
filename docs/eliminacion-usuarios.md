# Eliminación de Usuarios

## Resumen

Funcionalidad para eliminar usuarios del sistema VOCES, incluyendo endpoint backend y botón en la interfaz de usuario con confirmación de seguridad.

## Endpoint Backend

### Ruta: `POST /usuarios/{username}/eliminar`

**Ubicación:** `app/routes/usuarios.py`

**Descripción:** Elimina un usuario del sistema junto con su perfil demográfico asociado.

**Parámetros:**
- `username` (str): Nombre de usuario a eliminar

**Respuestas:**
- `303 See Other`: Redirección exitosa a `/usuarios`
- `404 Not Found`: Usuario no encontrado

**Ejemplo de uso:**
```python
@router.post("/{username}/eliminar")
async def eliminar_usuario(
    username: str, request: Request, session: AsyncSession = Depends(get_session)
):
    # Buscar el usuario
    statement = select(Usuario).where(Usuario.username == username)
    result = await session.execute(statement)
    usuario = result.scalars().first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Eliminar el usuario (eliminación en cascada del perfil demográfico)
    await session.delete(usuario)
    await session.commit()

    # Redirigir a la lista de usuarios
    return RedirectResponse(url="/usuarios", status_code=303)
```

## Interfaz de Usuario

### Ubicación: `app/templates/usuarios/perfil.html`

**Botón de Eliminar:**
- Se encuentra junto al botón "Editar" en la parte superior del perfil
- Estilo destructivo (rojo) para indicar acción peligrosa
- Incluye confirmación JavaScript antes de ejecutar la acción

**Código:**
```html
<form action="/usuarios/{{ usuario.username }}/eliminar" method="POST" 
    onsubmit="return confirm('¿Estás seguro de que deseas eliminar este usuario? Esta acción no se puede deshacer.');">
    <button type="submit"
        class="inline-flex items-center px-4 py-2 border border-destructive rounded-md text-sm font-medium text-destructive bg-background hover:bg-destructive hover:text-destructive-foreground transition-colors">
        <span class="material-symbols-outlined text-base mr-2">delete</span>
        Eliminar
    </button>
</form>
```

## Flujo de Uso

1. Usuario navega al perfil (`/usuarios/{username}`)
2. Hace clic en el botón "Eliminar"
3. Aparece diálogo de confirmación JavaScript
4. Si confirma:
   - Se envía POST a `/usuarios/{username}/eliminar`
   - Backend elimina usuario y perfil demográfico
   - Redirección a lista de usuarios (`/usuarios`)

## Características de Seguridad

### Implementadas
- ✅ Confirmación JavaScript antes de eliminar
- ✅ Mensaje claro sobre irreversibilidad de la acción
- ✅ Eliminación en cascada del perfil demográfico
- ✅ Validación de existencia del usuario

### Pendientes (Recomendadas para Producción)
- ⚠️ Verificación de permisos (solo Admin debería poder eliminar)
- ⚠️ Protección CSRF
- ⚠️ Log de auditoría
- ⚠️ Soft-delete en lugar de eliminación permanente
- ⚠️ Prevenir auto-eliminación del usuario actual

## Consideraciones Técnicas

### Eliminación en Cascada
La eliminación del usuario automáticamente elimina el perfil demográfico asociado gracias a la configuración de relaciones en SQLModel.

### Redirección
Se usa código de estado `303 See Other` para la redirección POST-redirect-GET, que es la práctica recomendada después de operaciones POST exitosas.

## Mejoras Futuras

1. **Sistema de Permisos**
   ```python
   # Verificar que el usuario actual sea Admin
   if usuario_actual.rol != Rol.Admin:
       raise HTTPException(status_code=403, detail="No tienes permisos")
   ```

2. **Soft Delete**
   ```python
   # En lugar de eliminar, marcar como inactivo
   usuario.estado_cuenta = EstadoCuenta.Eliminado
   usuario.fecha_eliminacion = datetime.utcnow()
   ```

3. **Log de Auditoría**
   ```python
   # Registrar la acción
   log_auditoria = LogAuditoria(
       accion="ELIMINAR_USUARIO",
       usuario_id=usuario_actual.id,
       objetivo_id=usuario.id,
       timestamp=datetime.utcnow()
   )
   session.add(log_auditoria)
   ```

## Archivos Modificados

- `app/routes/usuarios.py` - Nuevo endpoint de eliminación
- `app/templates/usuarios/perfil.html` - Botón de eliminar
- `app/templates/layout/components/navbar.html` - Mejora de lógica de botones (cambio adicional)

## Fecha de Implementación

2 de diciembre de 2025
