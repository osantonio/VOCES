# Guía de Diseño: Sistema de Anchos Máximos

## Filosofía de Diseño

El proyecto VOCES utiliza un sistema de anchos máximos consistente para mantener la legibilidad y una experiencia visual coherente en todos los dispositivos.

## Reglas de Ancho

### 1. Base Layout (`base.html`)

**NO** aplicar restricciones de ancho en `<main>`:
```html
<main class="grow">
    {% block content %}{% endblock %}
</main>
```

**Razón:** Permite que cada template hijo tenga control total sobre su ancho según sus necesidades específicas.

### 2. Templates Hijos - Patrón Estándar

Cada template debe envolver su contenido en un contenedor con estas clases:

```html
{% block content %}
<div class="min-h-screen bg-background">
    <div class="px-4 sm:px-10 lg:px-20 flex flex-1 justify-center py-5 sm:py-10">
        <div class="flex flex-col w-full max-w-[960px] flex-1">
            <!-- Contenido aquí -->
        </div>
    </div>
</div>
{% endblock %}
```

### 3. Anchos Máximos por Tipo de Contenido

| Tipo de Contenido | Ancho Máximo | Uso |
|-------------------|--------------|-----|
| **Contenido de lectura** | `max-w-[960px]` (60rem) | Perfiles, artículos, formularios |
| **Dashboards/Tablas** | `max-w-6xl` (80rem) | Listados amplios, dashboards |
| **Landing pages** | `max-w-6xl` (80rem) | Páginas de inicio, marketing |
| **Formularios estrechos** | `max-w-2xl` (42rem) | Login, registro |

### 4. Sistema de Padding Responsivo

**Patrón recomendado:**
```html
px-4 sm:px-10 lg:px-20
```

**Equivalencias:**
- `px-4` = 1rem (16px) en mobile
- `sm:px-10` = 2.5rem (40px) en tablet (≥640px)
- `lg:px-20` = 5rem (80px) en desktop (≥1024px)

### 5. Breakpoints de Tailwind

```
sm: 640px   (tablet pequeña)
md: 768px   (tablet)
lg: 1024px  (laptop)
xl: 1280px  (desktop)
2xl: 1536px (pantalla grande)
```

## Ejemplos por Template

### Perfil de Usuario (`perfil.html`)

```html
{% block content %}
<div class="min-h-screen bg-background">
    <div class="px-4 sm:px-10 lg:px-20 flex flex-1 justify-center py-5 sm:py-10">
        <div class="flex flex-col w-full max-w-[960px] flex-1">
            <!-- Contenido del perfil -->
        </div>
    </div>
</div>
{% endblock %}
```

**Comportamiento:**
- Mobile: ancho completo con padding de 16px
- Tablet: ancho completo con padding de 40px
- Desktop: máximo 960px centrado con padding de 80px

### Listado de Usuarios (`listar.html`)

```html
{% block content %}
<div class="min-h-screen bg-background">
    <div class="px-4 sm:px-10 lg:px-20 py-5 sm:py-10">
        <div class="max-w-6xl mx-auto">
            <!-- Tabla ancha -->
        </div>
    </div>
</div>
{% endblock %}
```

**Comportamiento:**
- Mobile: ancho completo con padding de 16px
- Tablet: ancho completo con padding de 40px
- Desktop: máximo 1280px (7xl) centrado con padding de 80px

### Login/Registro

```html
{% block content %}
<div class="w-full min-h-[calc(100vh-4rem)] lg:grid lg:grid-cols-2">
    <!-- Split screen layout -->
</div>
{% endblock %}
```

**Comportamiento:**
- Ancho completo para aprovechar el split-screen design

## Ventajas de Este Sistema

✅ **Flexibilidad:** Cada template controla su propio ancho
✅ **Consistencia:** Patrones reutilizables y predecibles
✅ **Responsive:** Adaptación natural a todos los tamaños
✅ **Legibilidad:** Anchos optimizados para lectura
✅ **Mantenibilidad:** Fácil de entender y modificar

## Anti-Patrones a Evitar

❌ **NO** aplicar `max-w` en `base.html`:
```html
<!-- MAL -->
<main class="grow max-w-6xl mx-auto">
```

❌ **NO** usar anchos fijos en píxeles:
```html
<!-- MAL -->
<div style="max-width: 1200px">
```

❌ **NO** mezclar múltiples niveles de `max-w`:
```html
<!-- MAL -->
<div class="max-w-6xl">
    <div class="max-w-5xl">
        <!-- Confuso y redundante -->
    </div>
</div>
```

## Checklist de Implementación

Al crear un nuevo template:

- [ ] Remover cualquier `max-w` de `base.html`
- [ ] Envolver contenido en contenedor con padding responsivo
- [ ] Aplicar `max-w` apropiado según tipo de contenido
- [ ] Usar `mx-auto` para centrar
- [ ] Probar en mobile, tablet y desktop
- [ ] Verificar que el padding se ve bien en todos los tamaños

## Migración de Templates Existentes

Si encuentras templates con estructura antigua:

1. Verificar que `base.html` no tenga `max-w`
2. Agregar contenedor con padding responsivo
3. Aplicar `max-w` apropiado
4. Probar responsive design

## Fecha de Creación

2 de diciembre de 2025
