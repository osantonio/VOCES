# Solución de Errores Comunes

Este documento recopila errores frecuentes encontrados durante el desarrollo y sus soluciones.

## 1. `RuntimeError: Form data requires "python-multipart" to be installed`

### Síntoma
Al intentar iniciar sesión (`/auth/login`) o usar endpoints que dependen de `OAuth2PasswordRequestForm`, el servidor lanza este error.

### Causa
FastAPI utiliza la librería `python-multipart` para parsear datos de formularios (form-data), que es el formato estándar para el envío de credenciales en OAuth2. Esta librería no se instala automáticamente con FastAPI estándar.

### Solución
Instalar la librería faltante:
```bash
pip install python-multipart
```

---

## 2. `UserWarning: Field name "metadata" in "LogActividad" shadows an attribute in parent "SQLModel"`

### Síntoma
Al iniciar la aplicación, aparece una advertencia indicando que un campo `metadata` oculta un atributo del padre.

```text
UserWarning: Field name "metadata" in "LogActividad" shadows an attribute in parent "SQLModel"
```

### Causa
`SQLModel` (y su base `SQLAlchemy`) utiliza el atributo `metadata` internamente para almacenar la información del esquema de la base de datos (tablas, columnas, etc.). Definir un campo con el mismo nombre crea un conflicto y puede romper la funcionalidad del ORM.

### Solución
Renombrar el campo en el modelo. En nuestro caso, cambiamos `metadata` a `detalles`.

**Incorrecto:**
```python
class LogActividad(SQLModel, table=True):
    metadata: Optional[dict] = Field(...)  # ❌ Conflicto con SQLModel.metadata
```

**Correcto:**
```python
class LogActividad(SQLModel, table=True):
    detalles: Optional[dict] = Field(...)  # ✅ Seguro
```

---

## 3. `TypeError: Field() got an unexpected keyword argument 'pattern'`

### Síntoma
Error al iniciar la aplicación en modelos que usan validación de regex.

### Causa
Diferencias entre versiones de Pydantic (v1 vs v2) utilizadas por SQLModel. SQLModel puede no aceptar el argumento `pattern` directamente en `Field()` si está usando una versión subyacente que espera `regex` o si la validación debe pasarse a través de `schema_extra`.

### Solución
Usar `schema_extra` para definir el patrón de validación JSON Schema, asegurando compatibilidad.

```python
# Antes (Error)
twitter_handle: str = Field(pattern=r"^@?...")

# Después (Solución)
twitter_handle: str = Field(schema_extra={"pattern": r"^@?..."})
```
