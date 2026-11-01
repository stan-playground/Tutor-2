# Stage 1 local authentication evidence

2 November 2026. This block implements local synthetic OIDC login through Keycloak and Authlib, database sessions, invitation checks, CSRF and logout. Application behavior and code are owned by [auth.py](../../../src/tutor_copilot/auth.py), [migration 0003](../../../migrations/versions/0003_auth.py) and the [real authentication tests](../../../tests/integration/test_auth.py). The parent Stage 1 record owns overall readiness and independent review.

## Architecture and limits

The fixed local issuer is `http://127.0.0.1:58080/realms/tutor-copilot`; the callback is `http://127.0.0.1:8000/auth/callback`. Keycloak uses a public OIDC client with authorization code, PKCE S256 and only the `openid` scope. Authlib validates state, nonce and the signed ID token using provider discovery/JWKS. The application matches the validated issuer/subject against two seeded synthetic invitations. A third synthetic identity can authenticate at Keycloak but cannot obtain an application session.

An opaque random cookie identifies a PostgreSQL session through its SHA-256 hash. Pending OIDC state remains server-side for ten minutes; an authenticated session lasts eight hours. Successful login rotates the token and retains no provider access/ID token or PKCE state. Every authenticated request checks session expiry and whether the invitation remains enabled. All unsafe authenticated methods require the session's CSRF token; browser Origin and cross-site fetch metadata are also checked. Logout deletes the database session.

Database sessions make revocation and logout immediate and avoid an application cookie-signing secret. Compared with signed cookies, this adds a database read per authenticated request. Local application passwords would add password recovery/security responsibilities already handled by the selected OIDC provider; no extra identity abstraction is introduced.

This application binds to loopback and deliberately uses HTTP for synthetic development. Its cookie is HttpOnly, SameSite=Lax and not Secure; production HTTPS cookies, identity terms, hosting and activation remain unverified. Keycloak has no persistent volume or bootstrap administrator; recreating its container reimports the generated synthetic realm. Credentials exist only in the ignored runtime import, are generated/consumed programmatically and are never printed or committed.

## Methods and lifetimes

| Method | Purpose, input, output and caller | Separation, errors and lifetime |
| --- | --- | --- |
| `token_hash(token)` | Converts one random bearer token to its database lookup hash; called by session creation, authorization, callback and logout. | Shares the exact lookup format without retaining a bearer token. Pure, request-local value; no I/O. |
| `create_session(database, tutor_id, oauth_data)` | Login/callback provide the application engine and either pending state or an invited tutor ID; returns a new opaque token. | Owns one short insert/expired-session cleanup transaction. Database errors propagate to the sanitized web error boundary. Engine lives for the application; transaction/data/token belong to this action. |
| `require_tutor(request)` | API dependencies and auth endpoints supply a request; returns a UUID after session/invitation/CSRF checks. | One shared authorization boundary for every learner route. Missing, expired or revoked sessions return 401; invalid CSRF/origin returns 403. It holds no transaction across endpoint work. |
| `set_session_cookie(response, token, pending)` | Login/callback provide a response and new token; sets the bounded local cookie and no-store header. | Keeps cookie attributes consistent. Mutates only the response being returned. |
| `install_auth(app)` | Application creation registers the provider and routes; returns nothing. | One Authlib registry/client configuration per FastAPI application. Provider calls use async I/O; no request is retained on the application object. |
| `login(request)` | Browser GET begins authorization, saves pending state and returns the provider redirect. | Ten-minute pending session; provider failure returns sanitized 503. No database transaction stays open during provider discovery. |
| `callback(request)` | Browser GET supplies the authorization response and pending cookie; consumes that pending state, validates OIDC, checks invitation and returns a new session/303 redirect. | Invalid/expired/replayed state returns 401; valid but uninvited identity returns 403. State is consumed once before provider exchange. Request-local tokens are discarded after identity validation. |
| `me(request)` | Browser GET returns the authenticated tutor UUID and CSRF token with no-store. | Calls the shared authorization boundary; values belong to the current browser session. |
| `logout(request)` | Browser POST supplies cookie/CSRF; deletes its session, expires the cookie and returns 204. | Uses the same authorization/CSRF check. Its database transaction is request-local. |
| `prepare()` | The developer runs the provisioning script; it refreshes the non-secret realm template, preserving existing synthetic credentials or generating new ones, and atomically writes the ignored import. | Separate because provisioning is not a web operation. File/JSON errors stop provisioning. Short-lived script; exclusive temporary creation prevents silently overwriting an interrupted write. |
| `LoginForm` / `complete_keycloak_login` | Integration tests parse the actual provider HTML and submit generated synthetic credentials internally, then deliver the actual authorization callback to the app. | Test-only transport, not a second identity implementation. It asserts PKCE and the exact callback path; failure diagnostics use fixed categories, never provider bodies/cookie values. |

Async I/O fits the real provider and PostgreSQL waits. Authentication does not need threads or processes. The synchronous provisioning script performs only small local file operations.

## Commands and original reports

```bash
UV_CACHE_DIR=.uv-cache uv add 'authlib>=1.6,<2' 'httpx>=0.28,<1'
python3 dev/keycloak/prepare.py
docker compose --env-file /dev/null -f compose.yaml up -d --wait keycloak
UV_CACHE_DIR=.uv-cache uv run --locked ruff check src/tutor_copilot/auth.py migrations/versions/0003_auth.py tests/integration/test_auth.py dev/keycloak/prepare.py
UV_CACHE_DIR=.uv-cache uv run --locked mypy src/tutor_copilot/auth.py migrations/versions/0003_auth.py
UV_CACHE_DIR=.uv-cache uv run --locked pytest tests/integration/test_auth.py -q --tb=short
```

The tested lock contains Authlib 1.9.1 and HTTPX 0.28.1. Compose pins Keycloak 26.8.1 to `sha256:3f3c5f8e03c614774b4bd9173b88391fefa4153bfc010d8012d59ad825377332`. PostgreSQL tests create/drop isolated random databases through the existing fixture; they do not delete the development database.

- [Initial diagnostic failure](auth-diagnosis-v1.txt): the real provider returned `Cookie not found`; HTTPX does not implement browser loopback exceptions for Secure cookies. The final HTTP helper selects Keycloak's existing Safari-compatible HTTP cookie policy with a Safari User-Agent. Provider/application security settings were not weakened for the test. [Versioned Keycloak implementation](https://github.com/keycloak/keycloak/blob/26.8.1/services/src/main/java/org/keycloak/utils/SecureContextResolver.java) documents this compatibility path.
- [First successful report](auth-v1.txt): three real integration tests passed after that transport fix and complete synthetic profile fields avoided an additional required-profile redirect.
- [State-mismatch coverage](auth-v2.txt): four tests passed after adding refusal/consumption of a wrong-state callback.
- [Final report](auth-v3.txt): four tests passed after keeping session/CSRF values out of assertion diagnostics. This is the current auth test input revision.

The checks cover actual code exchange/ID-token verification with Keycloak and actual PostgreSQL sessions, two invited identities, uninvited denial, PKCE, wrong state, callback replay, CSRF/origin, logout, expiry, invitation revocation and absence of retained OAuth state after login. The HTTP helper is not browser layout/accessibility or browser-engine QA; it does not prove a production provider, HTTPS deployment or real-learner readiness.
