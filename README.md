# TrustCore Test - Sistema de Gestión de Vulnerabilidades (Django + PostgreSQL)

## 1. Descripción General

Este proyecto es una API REST para la gestión de vulnerabilidades basada en datos de NIST/NVD. Permite listar, filtrar, marcar como solucionadas (fixed), deshacer fixes (unfixed), sincronizar datos y consultar métricas de seguridad.

Incluye autenticación JWT, rate limiting, auditoría y sincronización con NVD.

---

## 2. Requisitos previos

### Infraestructura

- Docker & Docker Compose (recomendado)
- PostgreSQL (si se ejecuta localmente)

> **⚠️ Importante**: PostgreSQL usa el puerto **5432** por defecto y Django el puerto **8000**, por lo que debes asegurarte de que estos puertos estén libres antes de ejecutar el proyecto.

### Backend

- Python 3.12+
- uv (gestor de dependencias)

### Herramientas y librerías usadas

- django>=6.0.5
- django-filter>=25.2
- djangorestframework>=3.17.1
- djangorestframework-simplejwt>=5.5.1
- drf-spectacular>=0.29.0
- psycopg[binary]>=3.3.4
- pytest>=9.0.3
- pytest-cov>=7.1.0
- pytest-django>=4.12.0
- python-dotenv>=1.2.2
- requests>=2.34.2

---

## 3. Arquitectura del Proyecto

El backend sigue una arquitectura tipo **Clean Architecture ligera**:

- Presentation: Views, Serializers, Endpoints
- Application: Services (casos de uso)
- Domain: Models y enums
- Infrastructure: ORM / PostgreSQL

---

## 4. Estructura del Proyecto

```bash
TRUSTCORE-TEST/
├── common/
│   ├── management/
│   │   └── commands/
│   │       └── seed.py
│   ├── migrations/
│   ├── apps.py
│   ├── auth_urls.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── api_router.py
│   ├── settings.py
│   └── urls.py
├── vulnerabilities/
│   ├── api/
│   │   └── nvd_sync_views.py
│   ├── management/
│   │   └── commands/
│   │       └── sync_nvd.py
│   ├── migrations/
│   ├── services/
│   │   ├── fixed_service.py
│   │   ├── nvd_sync_service.py
│   │   └── vulnerability_service.py
│   ├── tests/
│   ├── utils/
│   ├── admin.py
│   ├── apps.py
│   ├── constants.py
│   ├── models.py
│   ├── pagination.py
│   ├── serializers.py
│   ├── tests.py
│   ├── throttles.py
│   ├── urls.py
│   └── views.py
├── .env
├── docker-compose.yaml
├── dockerfile
├── manage.py
├── pyproject.toml
├── pytest.ini
├── requirements.txt
└── uv.lock
```

---

## 5. Endpoints disponibles

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

## 6. Ejemplos CURL

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "12345"}'
```

### List vulnerabilities

```bash
curl http://localhost:8000/api/v1/vulnerabilities/ \
  -H "Authorization: Bearer <access_token>"
```

### Active vulnerabilities

```bash
curl http://localhost:8000/api/v1/vulnerabilities/active/ \
  -H "Authorization: Bearer <access_token>"
```

### Mark as fixed

```bash
curl -X POST http://localhost:8000/api/v1/vulnerabilities/fixed/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"cve_ids": ["CVE-2024-1234"], "notes": "patched"}'
```

### Unfix vulnerability

```bash
curl -X DELETE http://localhost:8000/api/v1/vulnerabilities/unfixed/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"cve_id": "CVE-2024-1234"}'
```

### Summary

```bash
curl http://localhost:8000/api/v1/vulnerabilities/summary/ \
  -H "Authorization: Bearer <access_token>"
```

### Sync NVD

```bash
curl -X POST http://localhost:8000/api/v1/vulnerabilities/sync/ \
  -H "Authorization: Bearer <access_token>"
```

### Health check

```bash
curl http://localhost:8000/api/v1/health/
```

---

## 7. Migraciones y comandos

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

## 8. Variables de entorno

```env
DB_NAME=postgres
DB_USER=root
DB_PASSWORD=root
DB_HOST=db
DB_PORT=5432
```

---

## 9. Ejecución del proyecto

> **Requisito previo:** Después de clonar el repositorio, es obligatorio crear el archivo .env basado en .env.example, independientemente de si se ejecuta con Docker o de forma local.

### Con Docker (recomendado)

```bash
docker compose up --build
```

Esto levanta automáticamente:

- API Django
- Base de datos PostgreSQL
- Migraciones (si están configuradas en el entrypoint)

### Local

> **Requisito previo:** Debe existir una instancia de PostgreSQL ejecutándose localmente en el puerto 5432.

1. Instalar dependencias

```bash
uv sync
```

2. Aplicar migraciones

```bash
uv run python manage.py migrate
```

3. Cargar datos iniciales

```bash
uv run python manage.py seed
```

4. Sincronizar datos desde NVD

```bash
uv run python manage.py sync_nvd
```

5. Levantar el servidor

```bash
uv run python manage.py runserver
```

---

## 10. Dependencias y tooling

Este proyecto utiliza **uv** para la gestión de dependencias en Python por razones de rendimiento:

- Instalación más rápida que pip
- Mejor manejo de entornos virtuales
- Optimización en CI/CD y desarrollo local

---

## 11. Rate limiting (Throttling)

```python
DEFAULT_THROTTLE_RATES = {
    "anon": "100/day",
    "user": "1000/day",
    "fixed": "60/min",
    "sync": "5/min",
}
```

---

## 12. Consideraciones del sistema

- Login de prueba:

```json
{ "username": "admin", "password": "12345" }
```

- Sync NVD limitado a 100 registros
- Auditoría obligatoria en FIX / UNFIX / SYNC
- JWT válido por 6 horas

---

## 13. Swagger

http://localhost:8000/api/docs/

---

## 14. Modelo de Base de Datos

### vulnerabilities

- cve_id (unique): Identificador CVE
- description: Descripción de la vulnerabilidad
- severity: Nivel de severidad (CRITICAL, HIGH, MEDIUM, LOW, UNKNOWN)
- score: Puntaje CVSS (opcional)
- status: Estado (ACTIVE, FIXED, DEPRECATED)
- published_at: Fecha de publicación
- last_modified_at: Última modificación
- source: Fuente de datos (NVD)
- raw_payload: JSON original de NVD
- created_at: Fecha de creación en el sistema
- updated_at: Fecha de actualización

### fixed_vulnerabilities

**Relaciones:**

- vulnerability → Vulnerability
- fixed_by → Usuario (AUTH_USER_MODEL

- vulnerability (FK)
- fixed_by (FK)
- notes: Notas opcionales del fix
- fixed_at: Fecha de marcado como resuelto

**Restricción:**

- Unique (vulnerability, fixed_by)

### audit_logs

**Acciones soportadas:**

- FIX
- UNFIX
- SYNC

- user: Usuario que ejecuta la acción (nullable)
- action: Tipo de acción
- cve_id: Vulnerabilidad afectada
- metadata: Información adicional (JSON)
- created_at: Fecha del evento

---

## 15. Pruebas (pytest)

### Ejecución

```bash
pytest
```

### Cobertura

```bash
pytest --cov=vulnerabilities
```

- Cobertura aproximada: 70%
