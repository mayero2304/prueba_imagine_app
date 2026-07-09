# Prueba Imagine App

Aplicacion web para gestionar clientes y tickets de soporte, desarrollada como prueba tecnica para Finanz.

## Enlaces

- [Repositorio GitHub](https://github.com/mayero2304/prueba_imagine_app)
- [Tablero Kanban en GitHub](https://github.com/users/mayero2304/projects/4/views/1?layout=board)
- [PDF de la prueba](<PRUEBA TÉCNICA - DESARROLALDOR FINANZ.pdf>)
- [Flujo de la aplicacion](docs/flujo-aplicacion.md)
- [Modelo de datos y DER](docs/modelo-datos.md)
- [Coleccion Postman](docs/postman/PRUEBA_IMAGINE_APP.postman_collection.json)

## Alcance implementado

- Backend REST con Python, FastAPI y SQLAlchemy.
- Frontend con React y Vite.
- Base de datos PostgreSQL.
- Docker Compose para levantar PostgreSQL, backend y frontend.
- Frontend servido como build estatico con Nginx en Docker.
- Auditoria opcional de cambios de estado en MongoDB.
- Pruebas automatizadas con Pytest.
- Linters para backend y frontend.
- Pipeline CI con GitHub Actions.
- Coleccion Postman para probar la API.
- Documentacion con flujo de aplicacion y modelo ER en Mermaid.

## Arquitectura

```text
frontend React/Vite
        |
        | HTTP / JSON
        v
backend FastAPI
     |          |
     |          | eventos de auditoria opcionales
     |          v
     |       MongoDB
     |
     | SQLAlchemy
     v
PostgreSQL
```

En desarrollo local, Vite sirve el frontend con hot reload y FastAPI corre con `uvicorn --reload`.

En Docker, el frontend se compila primero y luego Nginx sirve los archivos estaticos generados por React. El backend corre como servicio independiente de FastAPI y se conecta a PostgreSQL dentro de la red de Docker Compose.

MongoDB se usa solo como valor agregado para auditoria. Si MongoDB no esta disponible, el cambio de estado del ticket sigue funcionando y el backend registra un warning en logs.

## Requisitos

Versiones usadas durante la entrega:

```text
Node.js:        26.4.0
npm:            11.16.0
Python:         3.11.14
Docker:         29.6.1
Docker Compose: 5.1.4
```

Todos los comandos siguientes se ejecutan desde la raiz del proyecto, salvo que se indique lo contrario.

## Ejecucion local para desarrollo

1. Instalar dependencias:

```bash
npm run install:all
```

2. Crear archivos de entorno:

```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

3. Levantar PostgreSQL:

```bash
npm run db:up
```

4. Preparar la base de datos con datos de prueba:

```bash
npm run db:fresh
```

Este comando borra el volumen local de PostgreSQL, crea una base limpia y carga clientes/tickets demo.

5. Levantar backend:

```bash
npm run dev:backend
```

6. Levantar frontend en otra terminal:

```bash
npm run dev:frontend
```

URLs locales:

- Frontend: <http://localhost:5173>
- Backend: <http://localhost:8000>
- Healthcheck: <http://localhost:8000/health>
- Swagger: <http://localhost:8000/docs>

## Ejecucion con Docker

Docker Compose construye y levanta PostgreSQL, backend y frontend.
Tambien levanta MongoDB para registrar auditoria de cambios de estado.

```bash
npm run docker:local:up
```

Comando equivalente:

```bash
docker compose up --build
```

URLs con Docker:

- Frontend: <http://localhost:5174>
- Backend: <http://localhost:8000>
- Healthcheck: <http://localhost:8000/health>
- Swagger: <http://localhost:8000/docs>
- MongoDB: `localhost:27017`

Apagar servicios:

```bash
npm run docker:local:down
```

Si el puerto `8000` ya esta ocupado:

```bash
BACKEND_PORT=8010 VITE_API_URL=http://localhost:8010 docker compose up --build
```

## Variables de entorno

Backend:

| Variable | Uso | Valor local sugerido |
| --- | --- | --- |
| `APP_NAME` | Nombre del servicio | `Imagine Support API` |
| `APP_ENV` | Entorno de ejecucion | `local` |
| `API_PREFIX` | Prefijo de rutas de API | `/api` |
| `DATABASE_URL` | Conexion SQLAlchemy a PostgreSQL | `postgresql+psycopg://postgres:postgres@localhost:5432/imagine_support` |
| `BACKEND_CORS_ORIGINS` | Origenes permitidos para CORS | `http://localhost:5173,http://localhost:5174` |
| `MONGO_AUDIT_ENABLED` | Activa o desactiva auditoria en MongoDB | `false` en local PC, `true` en Docker |
| `MONGO_URL` | Conexion a MongoDB | `mongodb://localhost:27017` |
| `MONGO_DATABASE` | Base de datos de auditoria | `imagine_support_audit` |
| `MONGO_AUDIT_COLLECTION` | Coleccion de eventos | `ticket_events` |

Frontend:

| Variable | Uso | Valor local sugerido |
| --- | --- | --- |
| `VITE_API_URL` | URL base del backend | `http://localhost:8000` |

Docker Compose:

| Variable | Uso | Valor por defecto |
| --- | --- | --- |
| `POSTGRES_DB` | Nombre de la base de datos | `imagine_support` |
| `POSTGRES_USER` | Usuario de PostgreSQL | `postgres` |
| `POSTGRES_PASSWORD` | Password de PostgreSQL | `postgres` |
| `POSTGRES_PORT` | Puerto local de PostgreSQL | `5432` |
| `BACKEND_PORT` | Puerto local del backend | `8000` |
| `FRONTEND_PORT` | Puerto local del frontend Docker | `5174` |
| `MONGO_PORT` | Puerto local de MongoDB | `27017` |
| `MONGO_AUDIT_ENABLED` | Activa auditoria al correr Docker Compose | `true` |
| `MONGO_DATABASE` | Base de datos de auditoria | `imagine_support_audit` |
| `MONGO_AUDIT_COLLECTION` | Coleccion de eventos | `ticket_events` |

## Endpoints principales

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| `GET` | `/health` | Verifica que la API este disponible. |
| `POST` | `/api/customers` | Crea un cliente. |
| `GET` | `/api/customers` | Lista clientes. |
| `GET` | `/api/customers/{customer_id}` | Consulta un cliente por ID. |
| `POST` | `/api/tickets` | Crea un ticket asociado a un cliente. |
| `GET` | `/api/tickets` | Lista tickets. |
| `PATCH` | `/api/tickets/{ticket_id}/status` | Actualiza el estado de un ticket. |

Estados permitidos para tickets:

```text
Pendiente -> En progreso -> Finalizado
```

El backend valida que no se salte de `Pendiente` directamente a `Finalizado`.

Cuando ocurre una transicion valida, el backend registra un evento de auditoria en MongoDB con:

- `ticket_id`
- `customer_id`
- `action`
- `previous_status`
- `new_status`
- `user`
- `occurred_at`

## Postman

Importar la coleccion:

```text
docs/postman/PRUEBA_IMAGINE_APP.postman_collection.json
```

La coleccion usa la variable `base_url`. Valor recomendado:

```text
http://localhost:8000
```

Orden recomendado para probar:

1. `Sistema -> Healthcheck`
2. `Clientes -> Crear cliente`
3. `Clientes -> Listar clientes`
4. `Clientes -> Consultar cliente por ID`
5. `Tickets -> Crear ticket`
6. `Tickets -> Listar tickets`
7. `Tickets -> Actualizar estado a En progreso`
8. `Tickets -> Actualizar estado a Finalizado`
9. `Validaciones -> Estado invalido`
10. `Validaciones -> Cliente inexistente`

## Base de datos y seed

Levantar solo PostgreSQL:

```bash
npm run db:up
```

Resetear PostgreSQL:

```bash
npm run db:reset
```

Cargar datos demo:

```bash
npm run db:seed
```

Resetear y cargar datos demo en un solo paso:

```bash
npm run db:fresh
```

## Auditoria en MongoDB

Con el stack Docker levantado, cambiar el estado de un ticket genera documentos en:

```text
database: imagine_support_audit
collection: ticket_events
```

Para revisar eventos desde la terminal:

```bash
docker compose exec mongo mongosh imagine_support_audit --eval "db.ticket_events.find().pretty()"
```

La auditoria esta desacoplada del flujo principal. Si MongoDB falla, el backend no cancela la actualizacion del ticket porque PostgreSQL sigue siendo la fuente principal de datos de la aplicacion.

## Calidad

Ejecutar linters:

```bash
npm run lint
```

Ejecutar pruebas:

```bash
npm test
```

Compilar frontend:

```bash
npm run build
```

Validacion completa local:

```bash
npm run lint
npm test
npm run build
```

## CI

El workflow de GitHub Actions esta en:

```text
.github/workflows/ci.yml
```

El pipeline corre en `push` y `pull_request` contra `main`:

- Backend: instala dependencias, ejecuta Ruff y Pytest.
- Frontend: instala dependencias, ejecuta ESLint y compila el build.

## Comandos disponibles

| Comando | Descripcion |
| --- | --- |
| `npm run install:all` | Instala dependencias de backend y frontend. |
| `npm run dev:backend` | Ejecuta FastAPI en modo desarrollo. |
| `npm run dev:frontend` | Ejecuta React/Vite en modo desarrollo. |
| `npm run db:up` | Levanta PostgreSQL con Docker Compose. |
| `npm run db:down` | Apaga los servicios de Docker Compose. |
| `npm run db:reset` | Borra el volumen local y levanta PostgreSQL limpio. |
| `npm run db:seed` | Carga clientes y tickets demo. |
| `npm run db:fresh` | Ejecuta reset y seed para iniciar pruebas desde cero. |
| `npm run db:logs` | Muestra logs de PostgreSQL. |
| `npm run lint` | Ejecuta linters de backend y frontend. |
| `npm test` | Ejecuta pruebas del backend. |
| `npm run build` | Compila el frontend. |
| `npm run docker:local:up` | Construye y levanta frontend, backend y PostgreSQL. |
| `npm run docker:local:down` | Apaga el stack Docker. |
| `npm run docker:local:logs` | Muestra logs del stack Docker. |

## Checklist de entrega

- [x] Backend FastAPI implementado.
- [x] Frontend React implementado.
- [x] PostgreSQL configurado.
- [x] Docker Compose configurado.
- [x] MongoDB de auditoria configurado como plus opcional.
- [x] Validacion de flujo de estados de tickets.
- [x] Manejo normalizado de errores.
- [x] Seed de datos para pruebas.
- [x] Coleccion Postman incluida.
- [x] Pruebas automatizadas incluidas.
- [x] Pipeline CI configurado.
- [x] README con comandos desde la raiz.
- [x] Diagrama de flujo y modelo ER documentados.
