from fastapi.testclient import TestClient


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
