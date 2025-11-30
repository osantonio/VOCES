# Guía de Validaciones en SQLModel y Pydantic v2

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Regla General: Field() vs @field_validator](#regla-general)
3. [Validaciones con Field()](#validaciones-con-field)
4. [Cuándo Usar @field_validator](#cuándo-usar-field_validator)
5. [Ejemplos Prácticos](#ejemplos-prácticos)
6. [Migración de Código Legacy](#migración-de-código-legacy)

---

## Introducción

Esta guía establece las mejores prácticas para validaciones en modelos SQLModel/Pydantic v2, siguiendo el **Zen de Python**: *"Simple es mejor que complejo"*.

### Principio Fundamental

> **Usa validaciones declarativas en `Field()` siempre que sea posible. Solo usa `@field_validator` para lógica compleja que no se puede expresar de forma declarativa.**

---

## Regla General

### ✅ Preferir: Validaciones Declarativas con `Field()`

**Ventajas:**
- Código más conciso y legible
- Validaciones visibles donde se define el campo
- Mejor rendimiento (validaciones nativas de Pydantic)
- Menos código que mantener
- Documentación automática en esquemas OpenAPI

### ❌ Evitar: `@field_validator` para validaciones simples

**Solo usar cuando:**
- La validación requiere lógica compleja
- Necesitas transformar el valor basándote en otros campos
- Requieres validaciones cruzadas entre múltiples campos

---

## Validaciones con Field()

### Parámetros Disponibles en `Field()`

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `min_length` | `int` | Longitud mínima de string | `min_length=3` |
| `max_length` | `int` | Longitud máxima de string | `max_length=50` |
| `pattern` | `str` | Regex para validar formato | `pattern=r"^[A-Z0-9]+$"` |
| `ge` | `int/float` | Mayor o igual que (≥) | `ge=0` |
| `gt` | `int/float` | Mayor que (>) | `gt=0` |
| `le` | `int/float` | Menor o igual que (≤) | `le=100` |
| `lt` | `int/float` | Menor que (<) | `lt=100` |
| `multiple_of` | `int/float` | Múltiplo de | `multiple_of=5` |

### Tipos Especiales de Pydantic

| Tipo | Validación | Requiere Instalación |
|------|------------|---------------------|
| `EmailStr` | Email válido (RFC 5322) | `pip install email-validator` |
| `HttpUrl` | URL HTTP/HTTPS válida | Incluido en Pydantic |
| `AnyUrl` | Cualquier URL válida | Incluido en Pydantic |
| `IPvAnyAddress` | Dirección IP válida | Incluido en Pydantic |
| `UUID` | UUID válido | Incluido en Pydantic |

---

## Ejemplos Prácticos

### 1. Email

#### ❌ **NO HACER** (Obsoleto)
```python
import re
from pydantic import field_validator

email: str = Field(unique=True, index=True)

@field_validator("email")
@classmethod
def validar_email(cls, valor: str) -> str:
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", valor):
        raise ValueError("Formato de email inválido")
    return valor.lower()
```

#### ✅ **HACER** (Moderno)
```python
from pydantic import EmailStr

email: EmailStr = Field(unique=True, index=True, max_length=255)
```

**Beneficios:**
- 9 líneas → 1 línea
- Validación RFC 5322 (más robusta)
- Normalización automática a minúsculas
- Sin imports adicionales de `re`

---

### 2. Username (Alfanumérico con guiones)

#### ❌ **NO HACER**
```python
import re
from pydantic import field_validator

username: str = Field(unique=True, max_length=50)

@field_validator("username")
@classmethod
def validar_username(cls, valor: str) -> str:
    if not re.match(r"^[a-zA-Z0-9_-]+$", valor):
        raise ValueError("Username inválido")
    return valor.lower()
```

#### ✅ **HACER**
```python
username: str = Field(
    unique=True,
    min_length=3,
    max_length=50,
    pattern=r"^[a-zA-Z0-9_-]+$",
)
```

**Beneficios:**
- 8 líneas → 5 líneas
- Validación declarativa
- Más fácil de leer y mantener

---

### 3. Password (Longitud mínima)

#### ❌ **NO HACER**
```python
from pydantic import field_validator

password: str = Field(exclude=True)

@field_validator("password")
@classmethod
def validar_password(cls, valor: str) -> str:
    if len(valor) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres")
    return valor
```

#### ✅ **HACER**
```python
password: str = Field(
    min_length=8,
    exclude=True,
)
```

**Beneficios:**
- 7 líneas → 3 líneas
- Validación nativa más eficiente

---

### 4. Edad (Rango numérico)

#### ❌ **NO HACER**
```python
from pydantic import field_validator

edad: int = Field()

@field_validator("edad")
@classmethod
def validar_edad(cls, valor: int) -> int:
    if valor < 18 or valor > 120:
        raise ValueError("Edad debe estar entre 18 y 120")
    return valor
```

#### ✅ **HACER**
```python
edad: int = Field(ge=18, le=120)
```

**Beneficios:**
- 7 líneas → 1 línea
- Más expresivo y claro

---

### 5. Precio (Positivo, múltiplo de 0.01)

#### ✅ **HACER**
```python
precio: float = Field(gt=0, multiple_of=0.01, description="Precio en USD")
```

---

## Cuándo Usar @field_validator

### ✅ Casos Válidos para `@field_validator`

#### 1. **Transformaciones Complejas**
```python
@field_validator("telefono")
@classmethod
def normalizar_telefono(cls, valor: str) -> str:
    """Elimina espacios, guiones y paréntesis"""
    return re.sub(r"[\s\-\(\)]", "", valor)
```

#### 2. **Validaciones Cruzadas**
```python
@field_validator("fecha_fin")
@classmethod
def validar_fecha_fin(cls, valor: datetime, info: ValidationInfo) -> datetime:
    """Valida que fecha_fin sea posterior a fecha_inicio"""
    if "fecha_inicio" in info.data and valor <= info.data["fecha_inicio"]:
        raise ValueError("fecha_fin debe ser posterior a fecha_inicio")
    return valor
```

#### 3. **Lógica de Negocio Compleja**
```python
@field_validator("codigo_postal")
@classmethod
def validar_codigo_postal(cls, valor: str, info: ValidationInfo) -> str:
    """Valida código postal según el país"""
    pais = info.data.get("pais")
    if pais == "CO" and not re.match(r"^\d{6}$", valor):
        raise ValueError("Código postal colombiano debe tener 6 dígitos")
    elif pais == "US" and not re.match(r"^\d{5}(-\d{4})?$", valor):
        raise ValueError("Código postal USA inválido")
    return valor
```

---

## Migración de Código Legacy

### Checklist de Migración

- [ ] **Identificar validadores simples** que solo verifican formato o longitud
- [ ] **Buscar tipos especiales de Pydantic** (EmailStr, HttpUrl, etc.)
- [ ] **Reemplazar regex simples** con parámetro `pattern` en Field()
- [ ] **Convertir validaciones de rango** a `ge`, `gt`, `le`, `lt`
- [ ] **Eliminar imports no utilizados** (`re`, `field_validator`)
- [ ] **Mantener validadores complejos** que requieren lógica de negocio
- [ ] **Probar las validaciones** con casos de prueba

### Ejemplo de Migración Completa

#### Antes (126 líneas)
```python
from datetime import datetime, timezone
from typing import Optional
from enum import Enum
import random
import string
import re  # ← Se puede eliminar
from sqlmodel import Field, SQLModel
from pydantic import field_validator  # ← Se puede eliminar

class Usuario(SQLModel, table=True):
    username: str = Field(unique=True, max_length=50)
    email: str = Field(unique=True, index=True)
    password: str = Field(exclude=True)
    
    @field_validator("email")
    @classmethod
    def validar_email(cls, valor: str) -> str:
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", valor):
            raise ValueError("Formato de email inválido")
        return valor.lower()
    
    @field_validator("password")
    @classmethod
    def validar_password(cls, valor: str) -> str:
        if len(valor) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return valor
    
    @field_validator("username")
    @classmethod
    def validar_username(cls, valor: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_-]+$", valor):
            raise ValueError("Username inválido")
        return valor.lower()
```

#### Después (102 líneas, -19% código)
```python
from datetime import datetime, timezone
from typing import Optional
from enum import Enum
import random
import string
from sqlmodel import Field, SQLModel
from pydantic import EmailStr  # ← Solo EmailStr

class Usuario(SQLModel, table=True):
    username: str = Field(
        unique=True,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_-]+$",
    )
    
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    
    password: str = Field(min_length=8, exclude=True)
```

**Mejoras:**
- ✅ -24 líneas de código (-19%)
- ✅ -2 imports innecesarios
- ✅ -3 funciones de validación
- ✅ Más declarativo y legible
- ✅ Mejor rendimiento

---

## Recursos Adicionales

### Documentación Oficial
- [Pydantic v2 - Field Types](https://docs.pydantic.dev/latest/api/types/)
- [Pydantic v2 - Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [SQLModel - Field Configuration](https://sqlmodel.tiangolo.com/tutorial/field/)

### Instalación de Dependencias
```bash
# Para usar EmailStr
pip install email-validator

# Para usar HttpUrl, IPvAnyAddress, etc. (ya incluido en Pydantic)
pip install pydantic
```

---

## Resumen de Mejores Prácticas

| ✅ HACER | ❌ NO HACER |
|---------|------------|
| Usar `EmailStr` para emails | Validar emails con regex manual |
| Usar `min_length`, `max_length` | Usar `@field_validator` para longitud |
| Usar `pattern` para regex simples | Usar `@field_validator` con `re.match()` |
| Usar `ge`, `le` para rangos | Usar `@field_validator` para comparaciones |
| Mantener validaciones donde se definen los campos | Dispersar validaciones en funciones separadas |
| Código declarativo y conciso | Código imperativo y verboso |

---

**Última actualización:** 2025-11-30  
**Versión de Pydantic:** v2.x  
**Versión de SQLModel:** 0.0.x
