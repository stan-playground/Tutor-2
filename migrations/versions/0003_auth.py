"""Add local invitations and database-backed browser sessions."""

from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE auth_invites (
            tutor_id uuid PRIMARY KEY,
            issuer text NOT NULL,
            subject text NOT NULL,
            enabled boolean NOT NULL DEFAULT true,
            UNIQUE (issuer, subject)
        );
        CREATE TABLE auth_sessions (
            token_hash text PRIMARY KEY,
            tutor_id uuid REFERENCES auth_invites(tutor_id) ON DELETE CASCADE,
            csrf_token text,
            oauth_data jsonb NOT NULL DEFAULT '{}',
            expires_at timestamptz NOT NULL,
            CHECK ((tutor_id IS NULL) = (csrf_token IS NULL))
        );
        CREATE INDEX auth_sessions_expiry ON auth_sessions(expires_at);
        INSERT INTO auth_invites (tutor_id, issuer, subject) VALUES
          ('11111111-1111-4111-8111-111111111111',
           'http://127.0.0.1:58080/realms/tutor-copilot',
           '10000000-0000-4000-8000-000000000001'),
          ('22222222-2222-4222-8222-222222222222',
           'http://127.0.0.1:58080/realms/tutor-copilot',
           '10000000-0000-4000-8000-000000000002');
        GRANT SELECT ON auth_invites TO tutor_app;
        GRANT SELECT, INSERT, DELETE ON auth_sessions TO tutor_app;
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE auth_sessions; DROP TABLE auth_invites")
