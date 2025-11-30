# VOCES - Plataforma de Blog Comunitario

Plataforma de blog comunitario con características de CMS y red social local, desarrollada con FastAPI, SQLModel y PostgreSQL.

## � Concepto

VOCES es una plataforma donde la comunidad crea y comparte contenido, similar a Digg:

- **Blog Comunitario:** Los usuarios pueden publicar sus propias entradas de blog
- **Reviews de Restaurantes:** Sistema editorial y de reviews generadas por usuarios
- **Gamificación:** Sistema de reputación y puntuación para motivar la participación
- **Roles Editoriales:** Contenido curado por editores y contribuciones de la comunidad

## �🚀 Características

- **Autenticación basada en sesiones** con gestión segura de usuarios
- **Sistema de roles** (Usuario, Editor, Admin) para control de permisos
- **Gestión de contenido** con capacidades de CMS
- **Sistema de reputación** para gamificación y motivación de usuarios
- **Interfaz moderna** con Tailwind CSS 4
- **Base de datos robusta** PostgreSQL con SQLModel
- **Validaciones avanzadas** con Pydantic v2

## 📋 Requisitos

- Python 3.10+
- PostgreSQL 12+
- Node.js (para Tailwind CSS)

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd VOCES
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

### 4. Instalar dependencias de Node.js

```bash
npm install
```

### 5. Configurar variables de entorno

Crea un archivo `.env` basado en `.env.example`:

```env
DATABASE_URL=postgresql://usuario:password@localhost/voces
SECRET_KEY=tu-clave-secreta-aqui
```

### 6. Ejecutar la aplicación

```bash
uvicorn main:app --reload
```

La aplicación estará disponible en `http://localhost:8000`

## 📚 Documentación

La documentación técnica del proyecto se encuentra en la carpeta [`docs/`](./docs/):

- **[Validaciones en SQLModel](./docs/validaciones-sqlmodel.md)** - Guía completa sobre mejores prácticas de validación usando `Field()` vs `@field_validator`

## 🏗️ Estructura del Proyecto

```
VOCES/
├── app/
│   ├── models/          # Modelos SQLModel
│   ├── routes/          # Rutas de la API
│   ├── static/          # Archivos estáticos (CSS, JS)
│   └── templates/       # Plantillas Jinja2
├── docs/                # Documentación técnica
├── main.py              # Punto de entrada de la aplicación
└── requirements.txt     # Dependencias de Python
```

## 🛠️ Tecnologías

- **Backend:** FastAPI, SQLModel, Pydantic v2
- **Base de datos:** PostgreSQL
- **Frontend:** Jinja2, Tailwind CSS 4
- **Validaciones:** Pydantic EmailStr, Field validators

## 📝 Desarrollo

### Mejores Prácticas

- Seguir el [Zen de Python](https://peps.python.org/pep-0020/)
- Usar validaciones declarativas en `Field()` cuando sea posible
- Nombres de variables descriptivos en español (evitar Ñ)
- Evitar código obsoleto o deprecado

### Ejecutar en modo desarrollo

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📄 Licencia

[Especificar licencia]

---

**Última actualización:** 2025-11-30
