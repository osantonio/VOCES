# Componente Navbar

Descripción: Barra de navegación reutilizable para VOCES con soporte de autenticación, accesibilidad y responsive.

Uso:
- Incluir en `layout/base.html` con `"{% include 'layout/components/navbar.html' %}"`.
- Requiere que `request` esté presente en el contexto de la plantilla.
- Si existe `request.state.usuario_actual`, se mostrará el menú de usuario.

Integración con autenticación:
- El middleware de la aplicación inyecta `request.state.usuario_actual` a partir de la cookie `access_token`.
- El avatar muestra `usuario_actual.avatar_url` si está disponible; de lo contrario, muestra iniciales usando `user_initials(usuario_actual)`.

Accesibilidad:
- Botón del menú con `aria-haspopup` y `aria-expanded`.
- Navegación por teclado: Enter/Espacio abre, Escape cierra.
- Cierre por clic fuera y tecla Escape.

Responsividad y estilos:
- Conserva clases utilitarias existentes (`bg-background`, `text-foreground`, etc.).
- Enlaces principales se ocultan en móviles (`hidden sm:flex`).
- Transiciones suaves del dropdown mediante clases `transition` y manipulación de `opacity/scale` en JS.

Enlaces del menú de usuario:
- `Perfil`: `/usuarios/{username}`
- `Dashboard`: `/dashboard`
- `Cerrar sesión`: `/auth/logout`

Dependencias:
- Íconos Material Symbols via Google Fonts.
- Script de modo oscuro (`static/js/dark-mode.js`).

Variables de contexto esperadas:
- `request`: objeto `Request` de Starlette.
- `request.state.usuario_actual`: instancia de `Usuario` o `None`.

