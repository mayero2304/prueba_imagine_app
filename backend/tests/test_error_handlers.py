from fastapi.testclient import TestClient

from app.main import create_app


def test_unknown_route_uses_normalized_http_error(client: TestClient) -> None:
    response = client.get("/api/unknown")
    body = response.json()

    assert response.status_code == 404
    assert body["statusCode"] == 404
    assert body["error"] == "Not Found"
    assert body["message"] == "Not Found"
    assert body["path"] == "/api/unknown"


def test_unhandled_error_uses_normalized_500_response() -> None:
    app = create_app(init_database=False)

    @app.get("/boom")
    def explode():
        raise RuntimeError("Sensitive internal detail")

    client = TestClient(app, raise_server_exceptions=False)

    response = client.get("/boom")
    body = response.json()

    assert response.status_code == 500
    assert body["statusCode"] == 500
    assert body["error"] == "Internal Server Error"
    assert body["message"] == "Internal Server Error"
    assert body["path"] == "/boom"
    assert "Sensitive internal detail" not in response.text
