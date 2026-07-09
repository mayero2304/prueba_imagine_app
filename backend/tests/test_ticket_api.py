from fastapi.testclient import TestClient

from app.services.audit_service import AuditService


def create_customer(client: TestClient) -> int:
    response = client.post(
        "/api/customers",
        json={
            "name": "Carlos Perez",
            "email": "carlos@example.com",
            "company": "Finanz",
        },
    )
    return int(response.json()["id"])


def test_create_list_and_update_ticket_status(client: TestClient) -> None:
    customer_id = create_customer(client)

    response = client.post(
        "/api/tickets",
        json={
            "customer_id": customer_id,
            "title": "Error al iniciar sesion",
            "description": "El cliente no puede acceder a la plataforma.",
        },
    )

    assert response.status_code == 201
    ticket = response.json()
    assert ticket["status"] == "Pendiente"

    update_response = client.patch(
        f"/api/tickets/{ticket['id']}/status",
        json={"status": "En progreso"},
    )

    assert update_response.status_code == 200
    assert update_response.json()["status"] == "En progreso"

    list_response = client.get("/api/tickets")

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_ticket_status_cannot_jump_from_pending_to_finished(
    client: TestClient,
) -> None:
    customer_id = create_customer(client)
    create_response = client.post(
        "/api/tickets",
        json={
            "customer_id": customer_id,
            "title": "Validar flujo",
            "description": "No debe saltar directamente a finalizado.",
        },
    )
    ticket = create_response.json()

    response = client.patch(
        f"/api/tickets/{ticket['id']}/status",
        json={"status": "Finalizado"},
    )

    assert response.status_code == 400
    assert response.json()["statusCode"] == 400
    assert response.json()["error"] == "Bad Request"
    assert (
        response.json()["message"]
        == "Invalid ticket status transition from Pendiente to Finalizado"
    )


def test_create_ticket_rejects_unknown_customer(client: TestClient) -> None:
    response = client.post(
        "/api/tickets",
        json={
            "customer_id": 999,
            "title": "Ticket sin cliente",
            "description": "Debe fallar porque el cliente no existe.",
        },
    )

    assert response.status_code == 404
    assert response.json()["statusCode"] == 404
    assert response.json()["error"] == "Not Found"
    assert response.json()["message"] == "Customer not found"
    assert response.json()["path"] == "/api/tickets"


def test_update_ticket_status_records_audit_event(
    client: TestClient,
    monkeypatch,
) -> None:
    recorded_events = []

    def record_ticket_status_change(_, **event):
        recorded_events.append(event)

    monkeypatch.setattr(
        AuditService,
        "record_ticket_status_change",
        record_ticket_status_change,
    )

    customer_id = create_customer(client)
    create_response = client.post(
        "/api/tickets",
        json={
            "customer_id": customer_id,
            "title": "Auditar estado",
            "description": "Debe registrar el cambio de estado en auditoria.",
        },
    )
    ticket = create_response.json()

    response = client.patch(
        f"/api/tickets/{ticket['id']}/status",
        json={"status": "En progreso"},
    )

    assert response.status_code == 200
    assert len(recorded_events) == 1
    assert recorded_events[0]["ticket_id"] == ticket["id"]
    assert recorded_events[0]["customer_id"] == customer_id
    assert recorded_events[0]["previous_status"].value == "Pendiente"
    assert recorded_events[0]["new_status"].value == "En progreso"
