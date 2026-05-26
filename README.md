# TrustCore Test - Sistema de Gestión de Vulnerabilidades (Django + PostgreSQL)

## 1. Descripción General

Este proyecto es una API REST para la gestión de vulnerabilidades basada en datos de NIST/NVD. Permite listar, filtrar, marcar como solucionadas (fixed), deshacer fixes (unfixed), sincronizar datos y consultar métricas de seguridad.

Incluye autenticación JWT, rate limiting, auditoría y sincronización con NVD.

---

## 2. Arquitectura del Proyecto

El backend sigue una arquitectura tipo **Clean Architecture ligera**:

- Presentation: Views, Serializers, Endpoints
- Application: Services (casos de uso)
- Domain: Models y enums
- Infrastructure: ORM / PostgreSQL

---

## 3. Endpoints disponibles

### Auth

- POST `/api/v1/auth/login/`
- POST `/api/v1/auth/refresh/`

### Health

- GET `/api/v1/health/`

### Vulnerabilities

- GET `/api/v1/vulnerabilities/`
- GET `/api/v1/vulnerabilities/active/`
- GET `/api/v1/vulnerabilities/summary/`

### Fixed flow

- POST `/api/v1/vulnerabilities/fixed/`
- DELETE `/api/v1/vulnerabilities/unfixed/`

### Sync

- POST `/api/v1/vulnerabilities/sync/`

---

## 4. Ejemplos CURL

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "12345"}'
```

---

### List vulnerabilities

```bash
curl http://localhost:8000/api/v1/vulnerabilities/ \
  -H "Authorization: Bearer <access_token>"
```

---

### Active vulnerabilities

```bash
curl http://localhost:8000/api/v1/vulnerabilities/active/ \
  -H "Authorization: Bearer <access_token>"
```

---

### Mark as fixed

```bash
curl -X POST http://localhost:8000/api/v1/vulnerabilities/fixed/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"cve_ids": ["CVE-2024-1234"], "notes": "patched"}'
```

---

### Unfix vulnerability

```bash
curl -X DELETE http://localhost:8000/api/v1/vulnerabilities/unfixed/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"cve_id": "CVE-2024-1234"}'
```

---

### Summary

```bash
curl http://localhost:8000/api/v1/vulnerabilities/summary/ \
  -H "Authorization: Bearer <access_token>"
```

---

### Sync NVD

```bash
curl -X POST http://localhost:8000/api/v1/vulnerabilities/sync/ \
  -H "Authorization: Bearer <access_token>"
```

---

### Health check

```bash
curl http://localhost:8000/api/v1/health/
```

---

## 5. Migraciones y comandos

### Migraciones

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

---

### Comandos del sistema

```bash
uv run python manage.py seed
uv run python manage.py sync_nvd
uv run python manage.py runserver
```

---

## 6. Variables de entorno

```env
DB_NAME=postgres
DB_USER=root
DB_PASSWORD=root
DB_HOST=db
DB_PORT=5432
```

> En Docker DB_HOST = `db`

---

## 7. Ejecución del proyecto

### Con Docker

```bash
docker compose up --build
```

### Local

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py seed
uv run python manage.py sync_nvd
uv run python manage.py runserver
```

---

## 8. Dependencias y tooling

Este proyecto utiliza **uv** para la gestión de dependencias en Python por razones de rendimiento:

- Instalación más rápida que pip
- Mejor manejo de entornos virtuales
- Optimización en CI/CD y desarrollo local

---

## 9. Rate limiting (Throttling)

```python
DEFAULT_THROTTLE_RATES = {
    "anon": "100/day",
    "user": "1000/day",
    "fixed": "60/min",
    "sync": "5/min",
}
```

---

## 10. Consideraciones del sistema

- Login de prueba:

```json
{
  "username": "admin",
  "password": "12345"
}
```

- Sync NVD limitado a 100 registros
- Unfix solo permite eliminar FIXED
- Auditoría obligatoria en FIX / UNFIX / SYNC
- Token JWT válido por 6 horas

---

## 11. Swagger

```
http://localhost:8000/api/docs/
```
