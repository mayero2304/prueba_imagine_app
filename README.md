# Prueba Imagine App

Aplicacion web para gestionar clientes y tickets de soporte, desarrollada como prueba tecnica para Finanz.

## Documentacion del proyecto

- [Tablero GitHub sugerido](docs/github-board.md)
- [PDF de la prueba](<PRUEBA TÉCNICA - DESARROLALDOR FINANZ.pdf>)

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
| [Local Docker](#local-docker) | Por completar cuando el backend y frontend esten listos para contenerizar. |

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

En esta primera base, Docker Compose levanta PostgreSQL para desarrollo local:

```bash
npm run docker:local:up
```

Apagar servicios:

```bash
npm run docker:local:down
```

El siguiente bloque del proyecto debe agregar `Dockerfile` para backend y frontend, de modo que el comando obligatorio de la prueba levante toda la solucion:

```bash
docker compose up
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
| `npm run db:up` | Levanta PostgreSQL con Docker Compose. |
| `npm run db:down` | Apaga los servicios de Docker Compose. |
| `npm run db:logs` | Muestra logs de PostgreSQL. |
| `npm run lint` | Ejecuta linters de backend y frontend. |
| `npm test` | Ejecuta pruebas del backend. |
| `npm run build` | Compila el frontend. |

## Siguiente orden de trabajo

1. Implementar modelos y persistencia PostgreSQL.
2. Crear endpoints de clientes.
3. Crear endpoints de tickets.
4. Construir vistas React para clientes y tickets.
5. Agregar pruebas unitarias e integracion.
6. Contenerizar backend y frontend.
7. Agregar GitHub Actions.
8. Completar `salesforce.md` como plus.
