"""Tutor-owned learner records, immutable evidence and frozen context."""

from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Roles belong to the local cluster, so concurrent isolated database tests serialize creation.
    op.execute("SELECT pg_advisory_xact_lock(730021)")
    op.execute("""
        DO $$ BEGIN
          IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'tutor_app') THEN
            CREATE ROLE tutor_app LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT;
          END IF;
        END $$;
        CREATE TABLE learners (
          id uuid PRIMARY KEY, tutor_id uuid NOT NULL, profile_revision integer NOT NULL,
          last_active timestamptz NOT NULL DEFAULT now()
        );
        CREATE TABLE profiles (
          learner_id uuid NOT NULL REFERENCES learners(id) ON DELETE CASCADE,
          tutor_id uuid NOT NULL, revision integer NOT NULL, data jsonb NOT NULL,
          PRIMARY KEY (learner_id, revision)
        );
        CREATE TABLE sources (
          id uuid PRIMARY KEY, learner_id uuid NOT NULL REFERENCES learners(id) ON DELETE CASCADE,
          revision integer NOT NULL DEFAULT 1,
          tutor_id uuid NOT NULL,
          kind text NOT NULL CHECK (kind IN ('lesson','homework','actual_use')),
          occurred_at timestamptz, qualification text NOT NULL,
          raw_text text, expires_at timestamptz NOT NULL DEFAULT now() + interval '30 days',
          fingerprint text NOT NULL
        );
        CREATE TABLE source_history (
          source_id uuid NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
          learner_id uuid NOT NULL REFERENCES learners(id) ON DELETE CASCADE,
          tutor_id uuid NOT NULL, revision integer NOT NULL, kind text NOT NULL,
          occurred_at timestamptz, qualification text NOT NULL, raw_text text,
          expires_at timestamptz NOT NULL, fingerprint text NOT NULL,
          PRIMARY KEY (source_id, revision)
        );
        CREATE TABLE observations (
          id uuid NOT NULL, revision integer NOT NULL, learner_id uuid NOT NULL
            REFERENCES learners(id) ON DELETE CASCADE,
          tutor_id uuid NOT NULL, source_id uuid NOT NULL REFERENCES sources(id),
          confirmed boolean NOT NULL, data jsonb NOT NULL,
          PRIMARY KEY (id, revision)
        );
        CREATE TABLE activities (
          id uuid NOT NULL, revision integer NOT NULL, learner_id uuid NOT NULL
            REFERENCES learners(id) ON DELETE CASCADE,
          tutor_id uuid NOT NULL, source_id uuid NOT NULL REFERENCES sources(id),
          confirmed boolean NOT NULL, data jsonb NOT NULL,
          PRIMARY KEY (id, revision)
        );
        CREATE TABLE contexts (
          id uuid PRIMARY KEY, learner_id uuid NOT NULL REFERENCES learners(id) ON DELETE CASCADE,
          tutor_id uuid NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), data jsonb NOT NULL
        );
        CREATE INDEX sources_learner_date ON sources(learner_id, occurred_at DESC, id);
        CREATE INDEX observations_learner ON observations(learner_id, id, revision DESC);
        CREATE INDEX activities_learner ON activities(learner_id, id, revision DESC);
        GRANT USAGE ON SCHEMA public TO tutor_app;
        GRANT SELECT ON alembic_version TO tutor_app;
    """)
    for table in (
        "learners",
        "profiles",
        "sources",
        "source_history",
        "observations",
        "activities",
        "contexts",
    ):
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY")
        parent_check = (
            ""
            if table == "learners"
            else (
                f" AND EXISTS (SELECT 1 FROM learners WHERE learners.id = {table}.learner_id "
                "AND learners.tutor_id::text = current_setting('app.tutor_id', true))"
            )
        )
        op.execute(f"""
            CREATE POLICY tutor_ownership ON {table}
              USING (tutor_id::text = current_setting('app.tutor_id', true){parent_check})
              WITH CHECK (tutor_id::text = current_setting('app.tutor_id', true){parent_check});
            GRANT SELECT, INSERT, UPDATE, DELETE ON {table} TO tutor_app;
        """)


def downgrade() -> None:
    for table in (
        "contexts",
        "activities",
        "observations",
        "source_history",
        "sources",
        "profiles",
        "learners",
    ):
        op.execute(f"DROP TABLE {table}")
