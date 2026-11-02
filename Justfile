set dotenv-load := false
set export
UV_CACHE_DIR := ".uv-cache"

default:
    @just --list

# Install the locked local environment; does not install Git hooks.
setup:
    uv sync --locked

# Download pinned public embedding weights anonymously; runtime inference stays offline.
embeddings-prepare:
    uv run --locked tutor-embeddings-prepare

# Start loopback-only synthetic development services; ignores implicit .env files.
up:
    docker compose --env-file /dev/null -f compose.yaml up -d --wait

# Prepare disposable synthetic identities and start the loopback OIDC provider.
auth-up:
    python3 dev/keycloak/prepare.py
    docker compose --env-file /dev/null -f compose.yaml up -d --wait keycloak

# Stop services and retain the PostgreSQL volume.
down:
    docker compose --env-file /dev/null -f compose.yaml --profile auth down

# Apply migrations to the fixed local development database.
migrate:
    uv run --locked alembic upgrade head

# Remove expired raw bodies/sessions and learners inactive for 12 calendar months.
cleanup:
    uv run --locked tutor-cleanup

web:
    uv run --locked tutor-web

worker:
    uv run --locked tutor-worker

format:
    uv run --locked ruff format src migrations tests

# Read-only checks; no service startup, migration or live provider calls.
check:
    uv run --locked ruff format --check src migrations tests
    uv run --locked ruff check src migrations tests
    uv run --locked mypy
    uv run --locked pytest tests/unit

# Real local services required; tests create and delete only random test databases/keys.
integration:
    uv run --locked pytest tests/integration
