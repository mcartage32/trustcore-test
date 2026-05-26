# TrustCore Test - Sistema de Gestión de Vulnerabilidades (Django + PostgreSQL)

## 1. Descripción General

Este proyecto es una API REST para la gestión de vulnerabilidades, basada en datos de NIST/NVD, con funcionalidades de listado, filtrado, marcado como solucionado (fixed), auditoría y exclusión de vulnerabilidades activas.

Incluye autenticación JWT, rate limiting, sincronización con NVD y pruebas automatizadas.

---

## 2. Arquitectura del Proyecto

El backend sigue una arquitectura por capas tipo **Clean Architecture ligera**:

- **Presentation**: Views, Serializers, Endpoints
- **Application**: Services (casos de uso)
- **Domain**: Models y enums
- **Infrastructure**: ORM / PostgreSQL

---

## 3. Estructura del proyecto

```text
trustcore-test/
├── config/
├── vulnerabilities/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── services/
│   ├── tests/
│   ├── management/commands/
│   │   └── sync_nvd.py
│   ├── throttles.py
│   └── utils/
├── docker-compose.yml
├── Dockerfile
├── manage.py
└── requirements.txt
```

---

## 4. Endpoints principales

### Vulnerabilities

- `GET /api/v1/vulnerabilities/`
- `GET /api/v1/vulnerabilities/active`
- `GET /api/v1/vulnerabilities/summary`

### Fixed

- `POST /api/v1/fixed`
- `DELETE /api/v1/unfix/{cve_id}`

### Sync

- `management command: sync_nvd`

---

## 5. Autenticación

Se usa JWT (SimpleJWT).

### Login

```json
{
  "username": "admin",
  "password": "12345"
}
```

El token tiene una vida útil de **6 horas**.

---

## 6. Filtros disponibles

- `cve_id`
- `severity` → CRITICAL | HIGH | MEDIUM | LOW | UNKNOWN
- `status` → ACTIVE | FIXED | DEPRECATED
- `published_from`
- `published_to`

---

## 7. Rate limiting (Throttling)

Se implementó throttling con Django REST Framework:

```python
"DEFAULT_THROTTLE_RATES": {
    "anon": "100/day",
    "user": "1000/day",
    "fixed": "60/min",
    "sync": "5/min"
}
```

---

## 8. Consideraciones importantes

### NVD API

- Solo se sincronizan **100 registros** por ejecución (modo prueba).

### Fixed vulnerabilities

- Al marcar como FIXED, la vulnerabilidad cambia su estado a `FIXED`.
- Al hacer UNFIX (DELETE lógico/físico de relación):
  - Se elimina de `fixed_vulnerabilities`
  - Se cambia el estado en `vulnerabilities` a `ACTIVE`
  - Se registra en `audit_logs`

### Eliminación (UNFIX)

- Se usa método `DELETE`
- Solo se puede eliminar si la vulnerabilidad está en estado `FIXED`
- Se registra auditoría completa:
  - usuario
  - acción
  - cve_id
  - metadata

---

## 9. Logs y auditoría

Cada acción importante genera registros en `audit_logs`:

- FIX
- UNFIX
- SYNC

Incluye:

- usuario
- acción
- cve_id
- metadata
- timestamp

---

## 10. Cache y configuración

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache"
    }
}
```

---

## 11. Docker

### Levantar proyecto

```bash
docker compose up --build
```

### Servicios

- Backend: http://localhost:8000
- DB: PostgreSQL en puerto 5432

---

## 12. Variables de entorno

```env
DB_NAME=postgres
DB_USER=root
DB_PASSWORD=root
DB_HOST=db
DB_PORT=5432
```

> En Docker: DB_HOST = `db`

---

## 13. Ejecución local

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py seed
uv run python manage.py sync_nvd
uv run python manage.py runserver
```

---

## 14. Testing

### Ejecutar tests

```bash
pytest
pytest --cov=vulnerabilities
```

### Cobertura mínima sugerida

- 70%+

---

## 15. Notas del sistema

- Login de prueba:

```json
{
  "username": "admin",
  "password": "12345"
}
```

- Rate limit configurado por endpoint
- Eliminación física solo en relación `FixedVulnerability`
- Sync inicial de NVD limitado a 100 registr
