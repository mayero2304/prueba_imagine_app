# Tablero GitHub - Prueba tecnica Finanz

## Lectura del PDF

La prueba pide una aplicacion web para gestionar clientes y tickets de soporte.

Stack obligatorio:

- Backend: Python con FastAPI.
- Frontend: React.
- Base de datos relacional: preferiblemente PostgreSQL.
- Docker: `docker compose up` debe levantar la solucion.
- Tests: minimo dos pruebas unitarias y una prueba de integracion.
- CI/CD: GitHub Actions con instalacion de dependencias, linter y pruebas.
- Git: multiples commits descriptivos, no un unico commit.

Valor agregado:

- MongoDB para auditoria de eventos.
- `salesforce.md` con propuesta tecnica de integracion Salesforce.

## Tablero recomendado

Columnas:

- Backlog
- To Do
- In Progress
- Review / QA
- Done

Milestones:

- `M1 - Backend y datos`: arquitectura backend, modelos, repositorios, servicios y endpoints.
- `M2 - Frontend e integracion`: vistas React e integracion con la API.
- `M3 - Calidad y entrega`: Docker, pruebas, CI/CD, README y validacion final.
- `Plus - Auditoria y Salesforce`: MongoDB de auditoria y documento Salesforce.

Labels:

| Label | Uso |
| --- | --- |
| `backend` | FastAPI, servicios, repositorios, schemas y endpoints. |
| `frontend` | React, componentes, formularios e integracion API. |
| `database` | PostgreSQL, modelos, migraciones y persistencia. |
| `docker` | Dockerfile, compose y variables de entorno. |
| `ci` | GitHub Actions, lint y pruebas en pipeline. |
| `tests` | Pruebas unitarias e integracion. |
| `docs` | README, instrucciones y documentacion tecnica. |
| `salesforce` | Documento opcional `salesforce.md`. |
| `audit` | Auditoria opcional con MongoDB. |
| `priority:p0` | Necesario para que el MVP sea entregable. |
| `priority:p1` | Importante para calidad y evaluacion. |
| `priority:p2` | Plus o mejora si queda tiempo. |
| `type:feature` | Funcionalidad nueva. |
| `type:chore` | Configuracion o estructura. |
| `type:test` | Cobertura automatizada. |
| `type:docs` | Documentacion. |

## Crear el tablero en GitHub

Si el repositorio ya existe en GitHub, ejecutar:

```bash
./scripts/create_github_board.sh mayero2304/NOMBRE_DEL_REPO mayero2304
```

Ejemplo con el nombre de esta carpeta:

```bash
./scripts/create_github_board.sh mayero2304/prueba_imagine_app mayero2304
```

El script crea o actualiza:

- Labels.
- Milestones.
- Proyecto de GitHub llamado `Prueba tecnica Finanz - Gestion clientes y tickets`.
- Issues con criterios de aceptacion.
- Vinculo entre el proyecto y el repositorio.

Si el repositorio remoto todavia no existe, una opcion segura es crearlo privado primero:

```bash
gh repo create mayero2304/prueba_imagine_app --private
```

Despues se puede ejecutar el script del tablero. Si la entrega necesita que el evaluador vea el repositorio, cambiarlo a publico o agregar acceso al evaluador desde GitHub.

## Issues sugeridos

### 1. `chore: initialize repository structure`

Labels: `type:chore`, `priority:p0`

Milestone: `M1 - Backend y datos`

Criterios de aceptacion:

- Repositorio inicializado con estructura separada para `backend/` y `frontend/`.
- Carpetas base del backend: `controllers/`, `services/`, `repositories/`, `models/`, `schemas/`.
- Configuracion inicial de `.gitignore`, variables de entorno de ejemplo y README base.
- Primer commit descriptivo.

Commit sugerido: `chore: initialize project structure`

### 2. `chore: configure Docker Compose services`

Labels: `docker`, `type:chore`, `priority:p0`

Milestone: `M3 - Calidad y entrega`

Criterios de aceptacion:

- `docker-compose.yml` levanta frontend, backend y PostgreSQL.
- Variables de conexion disponibles para backend.
- `docker compose up` arranca los servicios principales.
- Documentar puertos y comandos en README.

Commit sugerido: `chore: dockerize application`

### 3. `feat: setup FastAPI backend architecture`

Labels: `backend`, `type:feature`, `priority:p0`

Milestone: `M1 - Backend y datos`

Criterios de aceptacion:

- Aplicacion FastAPI inicial con router principal.
- Configuracion de settings por variables de entorno.
- Separacion por capas: controllers, services, repositories, models y schemas.
- Endpoint de healthcheck para validar el servicio.

Commit sugerido: `feat: setup fastapi backend architecture`

### 4. `feat: configure PostgreSQL persistence`

Labels: `backend`, `database`, `type:feature`, `priority:p0`

Milestone: `M1 - Backend y datos`

Criterios de aceptacion:

- Conexion a PostgreSQL desde FastAPI.
- Modelos ORM para clientes y tickets.
- Script/migracion o inicializacion clara de tablas.
- Relaciones entre cliente y tickets configuradas.

Commit sugerido: `feat: configure postgres persistence`

### 5. `feat: implement customer management API`

Labels: `backend`, `database`, `type:feature`, `priority:p0`

Milestone: `M1 - Backend y datos`

Criterios de aceptacion:

- Endpoint para crear cliente.
- Endpoint para listar clientes.
- Endpoint para consultar cliente por ID.
- Campos soportados: ID, nombre, correo electronico, empresa y fecha de creacion.
- Validaciones basicas con schemas.

Commit sugerido: `feat: create customer endpoints`

### 6. `feat: implement ticket management API`

Labels: `backend`, `database`, `type:feature`, `priority:p0`

Milestone: `M1 - Backend y datos`

Criterios de aceptacion:

- Endpoint para crear ticket asociado a cliente.
- Endpoint para listar tickets.
- Campos soportados: ID, cliente asociado, titulo, descripcion, estado y fecha de creacion.
- Validar que el cliente exista antes de crear el ticket.

Commit sugerido: `feat: implement ticket management`

### 7. `feat: update ticket status`

Labels: `backend`, `type:feature`, `priority:p0`

Milestone: `M1 - Backend y datos`

Criterios de aceptacion:

- Endpoint para actualizar estado de un ticket.
- Estados permitidos: `Pendiente`, `En progreso`, `Finalizado`.
- Rechazar estados invalidos con respuesta HTTP adecuada.
- Mantener la logica de negocio en service, no en controller.

Commit sugerido: `feat: add ticket status update`

### 8. `feat: bootstrap React frontend`

Labels: `frontend`, `type:feature`, `priority:p0`

Milestone: `M2 - Frontend e integracion`

Criterios de aceptacion:

- Proyecto React creado dentro de `frontend/`.
- Configuracion para consumir URL del backend desde variables de entorno.
- Estructura de componentes, servicios API y paginas/vistas.
- Vista principal con navegacion simple entre clientes y tickets.

Commit sugerido: `feat: create React app structure`

### 9. `feat: build customer views`

Labels: `frontend`, `type:feature`, `priority:p0`

Milestone: `M2 - Frontend e integracion`

Criterios de aceptacion:

- Vista para listar clientes.
- Formulario para registrar nuevo cliente.
- Integracion real con endpoints de clientes.
- Manejo basico de carga, exito y error.

Commit sugerido: `feat: create customer views`

### 10. `feat: build ticket views`

Labels: `frontend`, `type:feature`, `priority:p0`

Milestone: `M2 - Frontend e integracion`

Criterios de aceptacion:

- Vista para listar tickets.
- Formulario para crear ticket asociado a cliente.
- Control para actualizar estado del ticket.
- Integracion real con endpoints de tickets.

Commit sugerido: `feat: create ticket views`

### 11. `test: add backend unit tests`

Labels: `backend`, `tests`, `type:test`, `priority:p1`

Milestone: `M3 - Calidad y entrega`

Criterios de aceptacion:

- Minimo dos pruebas unitarias con Pytest.
- Cubrir logica de servicios o validaciones relevantes.
- Las pruebas corren de forma local y en CI.

Commit sugerido: `test: add backend unit tests`

### 12. `test: add API integration test`

Labels: `backend`, `tests`, `type:test`, `priority:p1`

Milestone: `M3 - Calidad y entrega`

Criterios de aceptacion:

- Minimo una prueba de integracion contra la API.
- Cubrir un flujo funcional, por ejemplo crear cliente y crear ticket asociado.
- Configuracion de base de datos de test o estrategia documentada.

Commit sugerido: `test: add api integration test`

### 13. `ci: add GitHub Actions pipeline`

Labels: `ci`, `tests`, `type:chore`, `priority:p1`

Milestone: `M3 - Calidad y entrega`

Criterios de aceptacion:

- Workflow en `.github/workflows/ci.yml`.
- Instala dependencias del backend.
- Ejecuta linter.
- Ejecuta pruebas automatizadas.
- Puede extenderse para frontend si queda tiempo.

Commit sugerido: `ci: add backend lint and test workflow`

### 14. `docs: write README execution guide`

Labels: `docs`, `type:docs`, `priority:p1`

Milestone: `M3 - Calidad y entrega`

Criterios de aceptacion:

- README con descripcion de la solucion.
- Instrucciones para levantar con `docker compose up`.
- Variables de entorno requeridas.
- Endpoints principales.
- Comandos para pruebas y lint.

Commit sugerido: `docs: add execution guide`

### 15. `qa: validate full delivery checklist`

Labels: `tests`, `docker`, `docs`, `priority:p1`

Milestone: `M3 - Calidad y entrega`

Criterios de aceptacion:

- Verificar que `docker compose up` funciona desde cero.
- Confirmar endpoints principales desde frontend o API client.
- Confirmar que CI pasa.
- Revisar que haya multiples commits descriptivos.
- Revisar que todos los entregables obligatorios esten presentes.

Commit sugerido: `chore: validate delivery checklist`

### 16. `feat: add MongoDB audit events`

Labels: `audit`, `database`, `type:feature`, `priority:p2`

Milestone: `Plus - Auditoria y Salesforce`

Criterios de aceptacion:

- Servicio MongoDB opcional en Docker Compose.
- Registrar eventos de auditoria al actualizar estado de ticket.
- Campos sugeridos: usuario, accion realizada, identificador del ticket, fecha y hora.
- La app sigue funcionando si se documenta como plus opcional.

Commit sugerido: `feat: add ticket audit events`

### 17. `docs: add Salesforce integration proposal`

Labels: `salesforce`, `docs`, `type:docs`, `priority:p2`

Milestone: `Plus - Auditoria y Salesforce`

Criterios de aceptacion:

- Crear `salesforce.md` de maximo una pagina.
- Incluir objetos Salesforce propuestos.
- Explicar informacion a sincronizar.
- Incluir ejemplo de Apex Trigger.
- Incluir ejemplo de componente LWC.
- Explicar exposicion mediante Experience Cloud.

Commit sugerido: `docs: add salesforce integration proposal`

## Orden recomendado para trabajar

1. Inicializar repo y estructura.
2. Backend base + PostgreSQL.
3. Clientes API.
4. Tickets API.
5. Frontend React basico.
6. Integracion frontend/API.
7. Tests minimos.
8. Docker Compose completo.
9. GitHub Actions.
10. README y validacion final.
11. Plus: MongoDB auditoria.
12. Plus: `salesforce.md`.

## Commits recomendados

Usar commits pequenos y descriptivos. Una secuencia aceptable seria:

```text
chore: initialize project structure
feat: setup fastapi backend architecture
feat: configure postgres persistence
feat: create customer endpoints
feat: implement ticket management
feat: add ticket status update
feat: create React app structure
feat: create customer views
feat: create ticket views
test: add backend unit tests
test: add api integration test
ci: add backend lint and test workflow
chore: dockerize application
docs: add execution guide
docs: add salesforce integration proposal
```
