"""Real Keycloak authorization-code login, PostgreSQL sessions and browser guards."""

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit

import httpx
from conftest import migrate
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from tutor_copilot.auth import COOKIE, ORIGIN
from tutor_copilot.web import create_app


class LoginForm(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.action = ""
        self.fields: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "form" and attributes.get("id") == "kc-form-login":
            self.action = attributes.get("action") or ""
        if tag == "input" and attributes.get("type") == "hidden" and attributes.get("name"):
            self.fields[str(attributes["name"])] = attributes.get("value") or ""


def complete_keycloak_login(
    client: TestClient, username: str, *, alter_state: bool = False
) -> tuple[int, str]:
    """Consume generated synthetic credentials internally; never display them."""
    started = client.get("/auth/login", follow_redirects=False)
    assert started.status_code == 302
    authorization = started.headers["location"]
    parameters = parse_qs(urlsplit(authorization).query)
    assert parameters["code_challenge_method"] == ["S256"]
    assert parameters.get("code_challenge")
    realm_file = Path(".highgrade/local/keycloak/tutor-copilot-realm.json")
    realm = json.loads(realm_file.read_text())
    synthetic = next(user for user in realm["users"] if user["username"] == username)
    # Keycloak's Safari compatibility path uses HTTP cookies; HTTPX has no browser
    # exception for Secure cookies on loopback. The provider still owns cookie policy.
    safari = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/18.6 Safari/605.1.15"
    )
    with httpx.Client(timeout=15, headers={"User-Agent": safari}) as browser:
        form_page = browser.get(authorization)
        assert form_page.status_code == 200
        form = LoginForm()
        form.feed(form_page.text)
        assert form.action, "Keycloak login form unavailable"
        browser_result = browser.post(
            form.action,
            data=form.fields
            | {"username": username, "password": synthetic["credentials"][0]["value"]},
        )
        known_errors = (
            "Cookie not found",
            "Invalid username or password",
            "Account is not fully set up",
            "HTTPS required",
            "Invalid requester",
            "Invalid request",
            "Unexpected error",
            "expired",
        )
        category = next(
            (value for value in known_errors if value.lower() in browser_result.text.lower()),
            "Unclassified provider error",
        )
        assert browser_result.status_code == 302, category
        location = urlsplit(browser_result.headers["location"])
        action = parse_qs(location.query).get("execution", [""])[0]
        required_action = action if action in {"UPDATE_PROFILE", "VERIFY_EMAIL"} else "other"
        assert location.path == "/auth/callback", required_action
    query = parse_qs(location.query)
    if alter_state:
        query["state"] = ["invalid-state"]
    callback = location.path + "?" + urlencode(query, doseq=True)
    completed = client.get(callback, follow_redirects=False)
    return completed.status_code, callback


def test_real_oidc_two_invited_tutors_and_uninvited_identity(database) -> None:
    migrate(database)
    with TestClient(create_app(database), base_url=ORIGIN) as first:
        assert first.get("/auth/me").status_code == 401
        assert complete_keycloak_login(first, "tutor-one")[0] == 303
        identity = first.get("/auth/me")
        assert identity.status_code == 200
        first_tutor = identity.json()["tutor_id"]
        assert first_tutor == "11111111-1111-4111-8111-111111111111"
        assert identity.headers["cache-control"] == "no-store"
        assert first.cookies.get(COOKIE)
        first_session = first.cookies.get(COOKIE)
    with TestClient(create_app(database), base_url=ORIGIN) as second:
        assert complete_keycloak_login(second, "tutor-two")[0] == 303
        second_tutor = second.get("/auth/me").json()["tutor_id"]
        assert second_tutor == "22222222-2222-4222-8222-222222222222"
        distinct_sessions = second.cookies.get(COOKIE) != first_session
        assert distinct_sessions
    with TestClient(create_app(database), base_url=ORIGIN) as outsider:
        assert complete_keycloak_login(outsider, "uninvited")[0] == 403
        assert outsider.get("/auth/me").status_code == 401
    admin = create_engine(database.database_url)
    try:
        with admin.connect() as connection:
            assert connection.scalar(text("SELECT count(*) FROM auth_sessions")) == 2
            assert connection.scalar(
                text("SELECT bool_and(oauth_data = '{}'::jsonb) FROM auth_sessions")
            )
    finally:
        admin.dispose()


def test_real_oidc_csrf_callback_replay_and_logout(database) -> None:
    migrate(database)
    with TestClient(create_app(database), base_url=ORIGIN) as client:
        status, callback = complete_keycloak_login(client, "tutor-one")
        assert status == 303
        replay = client.get(callback, follow_redirects=False)
        assert replay.status_code == 401
        csrf = client.get("/auth/me").json()["csrf_token"]
        assert client.post("/auth/logout").status_code == 403
        assert client.post("/auth/logout", headers={"X-CSRF-Token": "wrong"}).status_code == 403
        foreign_origin = client.post(
            "/auth/logout", headers={"X-CSRF-Token": csrf, "Origin": "https://other.invalid"}
        )
        assert foreign_origin.status_code == 403
        logged_out = client.post("/auth/logout", headers={"X-CSRF-Token": csrf, "Origin": ORIGIN})
        assert logged_out.status_code == 204
        assert client.get("/auth/me").status_code == 401


def test_real_session_expiry_and_invitation_revocation(database) -> None:
    migrate(database)
    admin = create_engine(database.database_url)
    try:
        with TestClient(create_app(database), base_url=ORIGIN) as client:
            assert complete_keycloak_login(client, "tutor-one")[0] == 303
            with admin.begin() as connection:
                connection.execute(text("UPDATE auth_invites SET enabled = false"))
            assert client.get("/auth/me").status_code == 401
            with admin.begin() as connection:
                connection.execute(text("UPDATE auth_invites SET enabled = true"))
                connection.execute(
                    text("UPDATE auth_sessions SET expires_at = now() - interval '1 second'")
                )
            assert client.get("/auth/me").status_code == 401
    finally:
        admin.dispose()


def test_real_oidc_refuses_wrong_state_and_consumes_pending_login(database) -> None:
    migrate(database)
    with TestClient(create_app(database), base_url=ORIGIN) as client:
        status, callback = complete_keycloak_login(client, "tutor-one", alter_state=True)
        assert status == 401
        assert client.get("/auth/me").status_code == 401
        replay = client.get(callback, follow_redirects=False)
        assert replay.status_code == 401
