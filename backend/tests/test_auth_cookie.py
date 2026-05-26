from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_login_sets_http_only_access_token_cookie() -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "teacher@example.com", "password": "password"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "user": {
            "id": 1,
            "name": "Demo Teacher",
            "email": "teacher@example.com",
            "role": "teacher",
            "is_active": True,
        }
    }
    assert "access_token" not in response.json()
    assert "access_token=" in response.headers["set-cookie"]
    assert "csrf_token=" in response.headers["set-cookie"]
    assert "HttpOnly" in response.headers["set-cookie"]
    assert "SameSite=lax" in response.headers["set-cookie"]


def test_me_reads_user_from_access_token_cookie() -> None:
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "password"},
    )

    response = client.get("/api/v1/auth/me")

    assert login_response.status_code == 200
    assert response.status_code == 200
    assert response.json()["user"]["email"] == "admin@example.com"
    assert response.json()["user"]["role"] == "admin"


def test_logout_clears_access_token_cookie() -> None:
    client.post(
        "/api/v1/auth/login",
        json={"email": "teacher@example.com", "password": "password"},
    )
    csrf_token = client.cookies.get("csrf_token")

    response = client.post(
        "/api/v1/auth/logout",
        headers={"X-CSRF-Token": csrf_token or ""},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Logged out"}
    assert "access_token=" in response.headers["set-cookie"]
    assert "csrf_token=" in response.headers["set-cookie"]
    assert "Max-Age=0" in response.headers["set-cookie"]


def test_state_changing_auth_route_rejects_missing_csrf_header() -> None:
    client.post(
        "/api/v1/auth/login",
        json={"email": "teacher@example.com", "password": "password"},
    )

    response = client.post("/api/v1/auth/logout")

    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid CSRF token"


def test_demo_password_reset_updates_login_password() -> None:
    forgot_response = client.post(
        "/api/v1/auth/forgot-password",
        json={"email": "teacher@example.com"},
    )
    reset_token = forgot_response.json()["reset_token"]

    reset_response = client.post(
        "/api/v1/auth/reset-password",
        json={"token": reset_token, "new_password": "new-password"},
    )
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "teacher@example.com", "password": "new-password"},
    )

    assert forgot_response.status_code == 200
    assert reset_response.status_code == 200
    assert login_response.status_code == 200
