"""Route-level account regressions beyond the prepared shared-helper checks."""

import pytest

from app import database


def member_session(client):
    """Create an isolated test member and authenticate through the real API."""
    credentials = {
        "username": "route_member",
        "password": "disposable route test passphrase",
    }
    token = client.get("/api/csrf").json()["csrf_token"]
    headers = {"X-CSRF-Token": token}
    assert (
        client.post("/api/signup", json=credentials, headers=headers).status_code == 201
    )
    assert (
        client.post("/api/login", json=credentials, headers=headers).status_code == 200
    )


@pytest.mark.parametrize("cookie", [None, "not-a-valid-session"])
def test_private_routes_do_not_show_content_without_a_valid_session(
    client, settings, cookie
):
    """Both missing and malformed sessions enforce the agreed HTML/API boundary."""
    if cookie:
        client.cookies.set(settings.cookie_name, cookie)
    page = client.get("/dashboard", follow_redirects=False)
    assert page.status_code == 303
    assert page.headers["location"] == "/login"
    assert "Your member space" not in page.text
    assert client.get("/api/me", follow_redirects=False).status_code == 401


def test_expired_server_session_blocks_both_private_routes(client, settings):
    """A still-signed cookie cannot bypass the stored session's expiry."""
    member_session(client)
    assert client.get("/dashboard").status_code == 200
    with database.connect(settings) as connection:
        connection.execute("UPDATE sessions SET expires_at = 0")
    assert client.get("/api/me").status_code == 401
    page = client.get("/dashboard", follow_redirects=False)
    assert page.status_code == 303
    assert page.headers["location"] == "/login"


def test_html_signup_cannot_choose_an_admin_role(client, settings):
    """The bounded three-field signup form rejects an injected fourth role field."""
    token = client.get("/api/csrf").json()["csrf_token"]
    response = client.post(
        "/signup",
        data={
            "username": "role_attempt",
            "password": "disposable route test passphrase",
            "role": "admin",
            "csrf_token": token,
        },
        follow_redirects=False,
    )
    assert response.status_code == 400
    with database.connect(settings) as connection:
        assert connection.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0
