from fastapi.testclient import TestClient


def test_create_and_list_customers(client: TestClient) -> None:
    response = client.post(
        "/api/customers",
        json={
            "name": "Ana Gomez",
            "email": "ana@example.com",
            "company": "Imagine",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "ana@example.com"

    list_response = client.get("/api/customers")

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_create_customer_rejects_duplicate_email(client: TestClient) -> None:
    payload = {
        "name": "Ana Gomez",
        "email": "ana@example.com",
        "company": "Imagine",
    }

    assert client.post("/api/customers", json=payload).status_code == 201
    response = client.post("/api/customers", json=payload)

    assert response.status_code == 409
    assert response.json()["statusCode"] == 409
    assert response.json()["error"] == "Conflict"
    assert response.json()["message"] == "Customer email already exists"
    assert response.json()["path"] == "/api/customers"


def test_create_customer_rejects_invalid_body(client: TestClient) -> None:
    response = client.post(
        "/api/customers",
        json={
            "name": "",
            "email": "invalid-email",
            "company": "Imagine",
        },
    )

    body = response.json()

    assert response.status_code == 422
    assert body["statusCode"] == 422
    assert body["error"] == "Unprocessable Entity"
    assert body["path"] == "/api/customers"
    assert isinstance(body["message"], list)
