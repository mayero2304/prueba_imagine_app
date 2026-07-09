# Prueba Imagine App

Aplicacion web para gestionar clientes y tickets de soporte, desarrollada como prueba tecnica para Finanz.

## Documentacion del proyecto

- [Repositorio GitHub](https://github.com/mayero2304/prueba_imagine_app)
- [Tablero Kanban en GitHub](https://github.com/users/mayero2304/projects/4/views/1?layout=board)
- [PDF de la prueba](<PRUEBA TÉCNICA - DESARROLALDOR FINANZ.pdf>)
- [Flujo de la aplicacion](docs/flujo-aplicacion.md)
- [Modelo de datos y DER](docs/modelo-datos.md)
- [Coleccion Postman](docs/postman/PRUEBA_IMAGINE_APP.postman_collection.json)

Para importar la coleccion en Postman, use el archivo:

```text
docs/postman/PRUEBA_IMAGINE_APP.postman_collection.json
```

Orden recomendado en Postman:

1. `Sistema -> Healthcheck`
2. `Clientes -> Crear cliente`
3. `Clientes -> Listar clientes`
4. `Clientes -> Consultar cliente por ID`
5. `Tickets -> Crear ticket`
6. `Tickets -> Listar tickets`
7. `Tickets -> Actualizar estado a En progreso`
8. `Tickets -> Actualizar estado a Finalizado`

## Alcance de la prueba

- Backend REST con Python y FastAPI.
- Frontend con React.
- Base de datos relacional con PostgreSQL.
- Docker Compose para levantar los servicios necesarios.
- Pruebas automatizadas con Pytest.
- Pipeline CI/CD con GitHub Actions.
- Documento opcional `salesforce.md`.

## Ejecucion rapida

Salvo que el bloque indique un `cd` especifico, ejecuta los comandos desde la raiz del proyecto.

| Modo | Uso recomendado |
| --- | --- |
| [Local PC](#local-pc) | Desarrollo con Node.js, Python y PostgreSQL local por Docker. |
| [Local Docker](#local-docker) | Levantar todo el stack construido con Docker Compose. |

### Local PC

Requisitos usados en esta entrega:

```text
Node.js:        26.4.0
npm:            11.16.0
Python:         3.11.14
Docker:         29.6.1
Docker Compose: 5.1.4
```

Instalar dependencias:

```bash
npm run install:all
```

Levantar PostgreSQL:

```bash
npm run db:up
```

Reiniciar la base de datos con datos de prueba:

```bash
npm run db:fresh
```

Este comando borra el volumen local de PostgreSQL, levanta una base limpia y carga clientes/tickets demo.

Configurar variables de entorno:

```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

Ejecutar backend y frontend en terminales separadas.

Terminal 1:

```bash
npm run dev:backend
```

Terminal 2:

```bash
npm run dev:frontend
```

URLs:

- Frontend: <http://localhost:5173>
- Backend: <http://localhost:8000>
- Healthcheck: <http://localhost:8000/health>
- Swagger: <http://localhost:8000/docs>

Verificacion local:

```bash
npm run lint
npm test
npm run build
```

### Local Docker

Docker Compose construye y levanta PostgreSQL, backend FastAPI y frontend React servido por Nginx:

```bash
npm run docker:local:up
```

Comando equivalente requerido por la prueba:

```bash
docker compose up --build
```

URLs:

- Frontend: <http://localhost:5174>
- Backend: <http://localhost:8000>
- Healthcheck: <http://localhost:8000/health>
- Swagger: <http://localhost:8000/docs>

Apagar servicios:

```bash
npm run docker:local:down
```

## Stack definido

- Backend: FastAPI.
- Frontend: React + Vite.
- Base de datos: PostgreSQL.
- Tests backend: Pytest.
- Linter backend: Ruff.
- Linter frontend: ESLint.

## Comandos disponibles

| Comando | Descripcion |
| --- | --- |
| `npm run install:all` | Instala dependencias de backend y frontend. |
| `npm run dev:backend` | Ejecuta FastAPI en modo desarrollo. |
| `npm run dev:frontend` | Ejecuta React/Vite en modo desarrollo. |
| `npm run db:up` | Levanta PostgreSQL con Docker Compose para desarrollo local. |
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

