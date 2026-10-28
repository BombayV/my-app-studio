"""Protected role payloads and navigation follow current server-side sessions."""

from app import database


def logged_in_member(client):
    """Create only a disposable member through the guarded account API."""
    credentials = {
        "username": "role_viewer",
        "password": "a disposable role test passphrase",
    }
    token = client.get("/api/csrf").json()["csrf_token"]
    headers = {"X-CSRF-Token": token}
    assert (
        client.post("/api/signup", json=credentials, headers=headers).status_code == 201
    )
    assert (
        client.post("/api/login", json=credentials, headers=headers).status_code == 200
    )


def test_role_changes_update_navigation_and_hide_admin_payload(client, settings):
    """A denied member retains member access but never gets the protected panel."""
    logged_in_member(client)
    assert 'href="/admin"' not in client.get("/dashboard").text
    denied = client.get("/admin")
    assert denied.status_code == 403
    assert "Access overview" not in denied.text
    assert client.get("/dashboard").status_code == 200
    assert database.set_role(settings, "role_viewer", "admin")
    assert 'href="/admin"' in client.get("/dashboard").text
    allowed = client.get("/admin")
    assert allowed.status_code == 200 and "Access overview" in allowed.text
    assert database.set_role(settings, "role_viewer", "member")
    denied = client.get("/admin")
    assert denied.status_code == 403 and "Access overview" not in denied.text
    assert client.get("/dashboard").status_code == 200


def test_a_revoked_admin_cookie_cannot_reopen_protected_routes(client, settings):
    """An administrator role does not rescue a session revoked at logout."""
    logged_in_member(client)
    assert database.set_role(settings, "role_viewer", "admin")
    assert client.get("/api/admin").status_code == 200
    copied = client.cookies.get(settings.cookie_name)
    token = client.get("/api/csrf").json()["csrf_token"]
    assert (
        client.post("/api/logout", headers={"X-CSRF-Token": token}).status_code == 200
    )
    client.cookies.set(settings.cookie_name, copied)
    assert client.get("/api/admin").status_code == 401
    page = client.get("/admin", follow_redirects=False)
    assert page.status_code == 303 and page.headers["location"] == "/login"
