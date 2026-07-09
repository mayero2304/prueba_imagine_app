#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Uso: $0 OWNER/REPO [PROJECT_OWNER]"
  echo "Ejemplo: $0 mayero2304/prueba_imagine_app mayero2304"
  exit 1
fi

REPO="$1"
PROJECT_OWNER="${2:-${REPO%%/*}}"
PROJECT_TITLE="Prueba tecnica Finanz - Gestion clientes y tickets"
TMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

echo "Validando repositorio $REPO..."
gh repo view "$REPO" >/dev/null

ensure_label() {
  local name="$1"
  local color="$2"
  local description="$3"

  if gh label list -R "$REPO" --json name --jq '.[].name' | grep -Fxq "$name"; then
    gh label edit "$name" -R "$REPO" --color "$color" --description "$description" >/dev/null
  else
    gh label create "$name" -R "$REPO" --color "$color" --description "$description" >/dev/null
  fi
}

ensure_milestone() {
  local title="$1"
  local description="$2"

  local number
  number="$(gh api "repos/$REPO/milestones?state=all&per_page=100" \
    --jq ".[] | select(.title == \"$title\") | .number" | head -n 1)"

  if [[ -z "$number" ]]; then
    gh api --method POST "repos/$REPO/milestones" \
      -f title="$title" \
      -f description="$description" >/dev/null
  fi
}

ensure_project() {
  local number
  number="$(gh project list --owner "$PROJECT_OWNER" --format json \
    --jq ".projects[] | select(.title == \"$PROJECT_TITLE\") | .number" | head -n 1)"

  if [[ -z "$number" ]]; then
    number="$(gh project create --owner "$PROJECT_OWNER" --title "$PROJECT_TITLE" --format json --jq '.number')"
  fi

  gh project link "$number" --owner "$PROJECT_OWNER" --repo "${REPO#*/}" >/dev/null 2>&1 || true
  echo "$number"
}

issue_exists() {
  local title="$1"
  gh issue list -R "$REPO" --state all --search "\"$title\" in:title" --json title \
    --jq ".[] | select(.title == \"$title\") | .title" | grep -Fxq "$title"
}

create_issue() {
  local title="$1"
  local labels="$2"
  local milestone="$3"
  local body="$4"
  local body_file="$TMP_DIR/body.md"

  if issue_exists "$title"; then
    echo "Ya existe: $title"
    return
  fi

  printf '%s\n' "$body" > "$body_file"

  echo "Creando issue: $title"
  gh issue create \
    -R "$REPO" \
    --title "$title" \
    --body-file "$body_file" \
    --label "$labels" \
    --milestone "$milestone" \
    --project "$PROJECT_TITLE" >/dev/null
}

echo "Creando/actualizando labels..."
ensure_label "backend" "0E8A16" "FastAPI, servicios, repositorios, schemas y endpoints."
ensure_label "frontend" "1D76DB" "React, componentes, formularios e integracion API."
ensure_label "database" "5319E7" "PostgreSQL, modelos, migraciones y persistencia."
ensure_label "docker" "006B75" "Dockerfile, compose y variables de entorno."
ensure_label "ci" "FBCA04" "GitHub Actions, lint y pruebas en pipeline."
ensure_label "tests" "D4C5F9" "Pruebas unitarias e integracion."
ensure_label "docs" "0075CA" "README, instrucciones y documentacion tecnica."
ensure_label "salesforce" "00A1E0" "Documento opcional salesforce.md."
ensure_label "audit" "BFDADC" "Auditoria opcional con MongoDB."
ensure_label "priority:p0" "B60205" "Necesario para que el MVP sea entregable."
ensure_label "priority:p1" "D93F0B" "Importante para calidad y evaluacion."
ensure_label "priority:p2" "C2E0C6" "Plus o mejora si queda tiempo."
ensure_label "type:feature" "A2EEEF" "Funcionalidad nueva."
ensure_label "type:chore" "F9D0C4" "Configuracion o estructura."
ensure_label "type:test" "D4C5F9" "Cobertura automatizada."
ensure_label "type:docs" "0075CA" "Documentacion."

echo "Creando milestones..."
ensure_milestone "M1 - Backend y datos" "Arquitectura backend, modelos, repositorios, servicios y endpoints."
ensure_milestone "M2 - Frontend e integracion" "Vistas React e integracion con la API."
ensure_milestone "M3 - Calidad y entrega" "Docker, pruebas, CI/CD, README y validacion final."
ensure_milestone "Plus - Auditoria y Salesforce" "MongoDB de auditoria y documento Salesforce."

echo "Creando/vinculando proyecto..."
PROJECT_NUMBER="$(ensure_project)"
echo "Proyecto: $PROJECT_TITLE (#$PROJECT_NUMBER)"

create_issue "chore: initialize repository structure" "type:chore,priority:p0" "M1 - Backend y datos" "$(cat <<'MD'
## Objetivo

Inicializar el repositorio y dejar la estructura base para desarrollar la prueba tecnica.

## Criterios de aceptacion

- [ ] Repositorio inicializado con estructura separada para `backend/` y `frontend/`.
- [ ] Carpetas base del backend: `controllers/`, `services/`, `repositories/`, `models/`, `schemas/`.
- [ ] Configuracion inicial de `.gitignore`, variables de entorno de ejemplo y README base.
- [ ] Primer commit descriptivo.

## Commit sugerido

`chore: initialize project structure`
MD
)"

create_issue "chore: configure Docker Compose services" "docker,type:chore,priority:p0" "M3 - Calidad y entrega" "$(cat <<'MD'
## Objetivo

Contenerizar la solucion para que pueda levantarse con `docker compose up`.

## Criterios de aceptacion

- [ ] `docker-compose.yml` levanta frontend, backend y PostgreSQL.
- [ ] Variables de conexion disponibles para backend.
- [ ] Los servicios principales arrancan desde cero.
- [ ] README documenta puertos y comandos.

## Commit sugerido

`chore: dockerize application`
MD
)"

create_issue "feat: setup FastAPI backend architecture" "backend,type:feature,priority:p0" "M1 - Backend y datos" "$(cat <<'MD'
## Objetivo

Crear la base de FastAPI con separacion de responsabilidades.

## Criterios de aceptacion

- [ ] Aplicacion FastAPI inicial con router principal.
- [ ] Configuracion de settings por variables de entorno.
- [ ] Separacion por capas: controllers, services, repositories, models y schemas.
- [ ] Endpoint de healthcheck para validar el servicio.

## Commit sugerido

`feat: setup fastapi backend architecture`
MD
)"

create_issue "feat: configure PostgreSQL persistence" "backend,database,type:feature,priority:p0" "M1 - Backend y datos" "$(cat <<'MD'
## Objetivo

Conectar FastAPI con PostgreSQL y definir la persistencia relacional.

## Criterios de aceptacion

- [ ] Conexion a PostgreSQL desde FastAPI.
- [ ] Modelos ORM para clientes y tickets.
- [ ] Script/migracion o inicializacion clara de tablas.
- [ ] Relacion entre cliente y tickets configurada.

## Commit sugerido

`feat: configure postgres persistence`
MD
)"

create_issue "feat: implement customer management API" "backend,database,type:feature,priority:p0" "M1 - Backend y datos" "$(cat <<'MD'
## Objetivo

Implementar la gestion de clientes requerida por el PDF.

## Criterios de aceptacion

- [ ] Endpoint para crear cliente.
- [ ] Endpoint para listar clientes.
- [ ] Endpoint para consultar cliente por ID.
- [ ] Campos: ID, nombre, correo electronico, empresa y fecha de creacion.
- [ ] Validaciones basicas con schemas.

## Commit sugerido

`feat: create customer endpoints`
MD
)"

create_issue "feat: implement ticket management API" "backend,database,type:feature,priority:p0" "M1 - Backend y datos" "$(cat <<'MD'
## Objetivo

Implementar la gestion de tickets asociados a clientes.

## Criterios de aceptacion

- [ ] Endpoint para crear ticket asociado a cliente.
- [ ] Endpoint para listar tickets.
- [ ] Campos: ID, cliente asociado, titulo, descripcion, estado y fecha de creacion.
- [ ] Validar que el cliente exista antes de crear el ticket.

## Commit sugerido

`feat: implement ticket management`
MD
)"

create_issue "feat: update ticket status" "backend,type:feature,priority:p0" "M1 - Backend y datos" "$(cat <<'MD'
## Objetivo

Permitir actualizar el estado de un ticket con validaciones claras.

## Criterios de aceptacion

- [ ] Endpoint para actualizar estado de un ticket.
- [ ] Estados permitidos: `Pendiente`, `En progreso`, `Finalizado`.
- [ ] Estados invalidos devuelven respuesta HTTP adecuada.
- [ ] La logica de negocio vive en service, no en controller.

## Commit sugerido

`feat: add ticket status update`
MD
)"

create_issue "feat: bootstrap React frontend" "frontend,type:feature,priority:p0" "M2 - Frontend e integracion" "$(cat <<'MD'
## Objetivo

Crear la base del frontend React para consumir la API.

## Criterios de aceptacion

- [ ] Proyecto React creado dentro de `frontend/`.
- [ ] URL del backend configurable por variables de entorno.
- [ ] Estructura de componentes, servicios API y paginas/vistas.
- [ ] Vista principal con navegacion simple entre clientes y tickets.

## Commit sugerido

`feat: create React app structure`
MD
)"

create_issue "feat: build customer views" "frontend,type:feature,priority:p0" "M2 - Frontend e integracion" "$(cat <<'MD'
## Objetivo

Construir la interfaz para clientes.

## Criterios de aceptacion

- [ ] Vista para listar clientes.
- [ ] Formulario para registrar nuevo cliente.
- [ ] Integracion real con endpoints de clientes.
- [ ] Manejo basico de carga, exito y error.

## Commit sugerido

`feat: create customer views`
MD
)"

create_issue "feat: build ticket views" "frontend,type:feature,priority:p0" "M2 - Frontend e integracion" "$(cat <<'MD'
## Objetivo

Construir la interfaz para tickets.

## Criterios de aceptacion

- [ ] Vista para listar tickets.
- [ ] Formulario para crear ticket asociado a cliente.
- [ ] Control para actualizar estado del ticket.
- [ ] Integracion real con endpoints de tickets.

## Commit sugerido

`feat: create ticket views`
MD
)"

create_issue "test: add backend unit tests" "backend,tests,type:test,priority:p1" "M3 - Calidad y entrega" "$(cat <<'MD'
## Objetivo

Agregar las pruebas unitarias minimas pedidas por la prueba.

## Criterios de aceptacion

- [ ] Minimo dos pruebas unitarias con Pytest.
- [ ] Cubrir logica de servicios o validaciones relevantes.
- [ ] Las pruebas corren localmente y en CI.

## Commit sugerido

`test: add backend unit tests`
MD
)"

create_issue "test: add API integration test" "backend,tests,type:test,priority:p1" "M3 - Calidad y entrega" "$(cat <<'MD'
## Objetivo

Agregar una prueba de integracion contra la API.

## Criterios de aceptacion

- [ ] Minimo una prueba de integracion.
- [ ] Cubrir un flujo funcional, por ejemplo crear cliente y crear ticket asociado.
- [ ] Configuracion de base de datos de test o estrategia documentada.

## Commit sugerido

`test: add api integration test`
MD
)"

create_issue "ci: add GitHub Actions pipeline" "ci,tests,type:chore,priority:p1" "M3 - Calidad y entrega" "$(cat <<'MD'
## Objetivo

Crear el pipeline basico exigido por el PDF.

## Criterios de aceptacion

- [ ] Workflow en `.github/workflows/ci.yml`.
- [ ] Instala dependencias del backend.
- [ ] Ejecuta linter.
- [ ] Ejecuta pruebas automatizadas.
- [ ] Puede extenderse para frontend si queda tiempo.

## Commit sugerido

`ci: add backend lint and test workflow`
MD
)"

create_issue "docs: write README execution guide" "docs,type:docs,priority:p1" "M3 - Calidad y entrega" "$(cat <<'MD'
## Objetivo

Documentar como ejecutar y validar la solucion.

## Criterios de aceptacion

- [ ] README con descripcion de la solucion.
- [ ] Instrucciones para levantar con `docker compose up`.
- [ ] Variables de entorno requeridas.
- [ ] Endpoints principales.
- [ ] Comandos para pruebas y lint.

## Commit sugerido

`docs: add execution guide`
MD
)"

create_issue "qa: validate full delivery checklist" "tests,docker,docs,priority:p1" "M3 - Calidad y entrega" "$(cat <<'MD'
## Objetivo

Hacer la revision final antes de entregar.

## Criterios de aceptacion

- [ ] `docker compose up` funciona desde cero.
- [ ] Endpoints principales validados desde frontend o API client.
- [ ] CI pasa.
- [ ] Existen multiples commits descriptivos.
- [ ] Todos los entregables obligatorios estan presentes.

## Commit sugerido

`chore: validate delivery checklist`
MD
)"

create_issue "feat: add MongoDB audit events" "audit,database,type:feature,priority:p2" "Plus - Auditoria y Salesforce" "$(cat <<'MD'
## Objetivo

Implementar el valor agregado de auditoria con MongoDB.

## Criterios de aceptacion

- [ ] Servicio MongoDB opcional en Docker Compose.
- [ ] Registrar eventos de auditoria al actualizar estado de ticket.
- [ ] Campos sugeridos: usuario, accion realizada, identificador del ticket, fecha y hora.
- [ ] La app sigue funcionando si se documenta como plus opcional.

## Commit sugerido

`feat: add ticket audit events`
MD
)"

create_issue "docs: add Salesforce integration proposal" "salesforce,docs,type:docs,priority:p2" "Plus - Auditoria y Salesforce" "$(cat <<'MD'
## Objetivo

Crear el documento opcional `salesforce.md` solicitado en el PDF.

## Criterios de aceptacion

- [ ] Archivo `salesforce.md` de maximo una pagina.
- [ ] Objetos Salesforce propuestos.
- [ ] Informacion que se sincronizaria.
- [ ] Ejemplo de Apex Trigger.
- [ ] Ejemplo de componente LWC.
- [ ] Explicacion de exposicion mediante Experience Cloud.

## Commit sugerido

`docs: add salesforce integration proposal`
MD
)"

echo "Listo. Revisa el proyecto en GitHub con:"
echo "gh project view \"$PROJECT_NUMBER\" --owner \"$PROJECT_OWNER\" --web"
