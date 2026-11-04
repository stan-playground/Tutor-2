"""Scope evidence identities by learner and retain exact source versions."""

from alembic import op

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Old evidence carries no source revision or creation time; do not invent one.
    op.execute("""
        LOCK TABLE learners, sources, source_history, observations, activities, contexts
          IN ACCESS EXCLUSIVE MODE;
        DO $$ BEGIN
          IF EXISTS (
            SELECT 1 FROM source_history h
            JOIN sources s ON s.id=h.source_id
            WHERE h.learner_id<>s.learner_id OR h.tutor_id<>s.tutor_id
          ) OR EXISTS (
            SELECT 1 FROM sources s JOIN learners l ON l.id=s.learner_id
            WHERE s.tutor_id<>l.tutor_id
          ) OR EXISTS (
            SELECT 1 FROM observations o JOIN sources s ON s.id=o.source_id
            WHERE o.learner_id<>s.learner_id OR o.tutor_id<>s.tutor_id
            UNION ALL
            SELECT 1 FROM activities a JOIN sources s ON s.id=a.source_id
            WHERE a.learner_id<>s.learner_id OR a.tutor_id<>s.tutor_id
          ) THEN
            RAISE EXCEPTION 'Stage 2R migration: mismatched learner or tutor source references';
          END IF;
          IF EXISTS (
            SELECT 1 FROM observations o JOIN source_history h ON h.source_id=o.source_id
            UNION ALL
            SELECT 1 FROM activities a JOIN source_history h ON h.source_id=a.source_id
            UNION ALL
            SELECT 1 FROM observations o JOIN sources s ON s.id=o.source_id WHERE s.revision<>1
            UNION ALL
            SELECT 1 FROM activities a JOIN sources s ON s.id=a.source_id WHERE s.revision<>1
          ) THEN
            RAISE EXCEPTION 'Stage 2R migration: ambiguous evidence source revision';
          END IF;
          IF EXISTS (
            SELECT 1 FROM observations WHERE data->>'source_id' IS DISTINCT FROM source_id::text
            UNION ALL
            SELECT 1 FROM activities WHERE data->>'source_id' IS DISTINCT FROM source_id::text
          ) THEN
            RAISE EXCEPTION 'Stage 2R migration: mismatched JSON source reference';
          END IF;
          IF EXISTS (
            SELECT 1 FROM activities a
            LEFT JOIN observations o ON o.learner_id=a.learner_id
              AND o.id=(a.data->>'observation_id')::uuid
              AND o.revision=(a.data->>'observation_revision')::integer
            WHERE (a.data->>'observation_id' IS NULL) <>
                  (a.data->>'observation_revision' IS NULL)
               OR (a.data->>'observation_id' IS NOT NULL AND o.id IS NULL)
          ) THEN
            RAISE EXCEPTION 'Stage 2R migration: invalid activity observation reference';
          END IF;
        END $$;

        ALTER TABLE source_history DROP CONSTRAINT source_history_source_id_fkey;
        ALTER TABLE observations DROP CONSTRAINT observations_source_id_fkey;
        ALTER TABLE activities DROP CONSTRAINT activities_source_id_fkey;
        ALTER TABLE sources DROP CONSTRAINT sources_pkey;
        ALTER TABLE sources ADD PRIMARY KEY (learner_id,id);
        CREATE TABLE source_versions (
          learner_id uuid NOT NULL, source_id uuid NOT NULL, revision integer NOT NULL,
          tutor_id uuid NOT NULL, kind text NOT NULL
            CHECK (kind IN ('lesson','homework','actual_use')),
          occurred_at timestamptz, qualification text NOT NULL, raw_text text,
          expires_at timestamptz NOT NULL, fingerprint text NOT NULL,
          PRIMARY KEY (learner_id,source_id,revision),
          FOREIGN KEY (learner_id,source_id) REFERENCES sources(learner_id,id) ON DELETE CASCADE
        );
        INSERT INTO source_versions
          SELECT learner_id,source_id,revision,tutor_id,kind,occurred_at,qualification,
                 raw_text,expires_at,fingerprint FROM source_history
          UNION ALL
          SELECT learner_id,id,revision,tutor_id,kind,occurred_at,qualification,
                 raw_text,expires_at,fingerprint FROM sources;
        ALTER TABLE source_versions ENABLE ROW LEVEL SECURITY;
        ALTER TABLE source_versions FORCE ROW LEVEL SECURITY;
        CREATE POLICY tutor_ownership ON source_versions
          USING (tutor_id::text = current_setting('app.tutor_id', true)
            AND EXISTS (SELECT 1 FROM learners WHERE learners.id=source_versions.learner_id
              AND learners.tutor_id::text=current_setting('app.tutor_id', true)))
          WITH CHECK (tutor_id::text = current_setting('app.tutor_id', true)
            AND EXISTS (SELECT 1 FROM learners WHERE learners.id=source_versions.learner_id
              AND learners.tutor_id::text=current_setting('app.tutor_id', true)));
        GRANT SELECT, INSERT ON source_versions TO tutor_app;
        REVOKE DELETE ON sources FROM tutor_app;

        ALTER TABLE observations ADD COLUMN source_revision integer;
        ALTER TABLE activities ADD COLUMN source_revision integer;
        UPDATE observations o SET source_revision=s.revision FROM sources s
          WHERE s.learner_id=o.learner_id AND s.id=o.source_id;
        UPDATE activities a SET source_revision=s.revision FROM sources s
          WHERE s.learner_id=a.learner_id AND s.id=a.source_id;
        ALTER TABLE observations ALTER COLUMN source_revision SET NOT NULL;
        ALTER TABLE activities ALTER COLUMN source_revision SET NOT NULL;
        ALTER TABLE observations DROP CONSTRAINT observations_pkey;
        ALTER TABLE observations ADD PRIMARY KEY (learner_id,id,revision);
        ALTER TABLE activities DROP CONSTRAINT activities_pkey;
        ALTER TABLE activities ADD PRIMARY KEY (learner_id,id,revision);
        ALTER TABLE observations ADD CONSTRAINT observations_source_version_fkey
          FOREIGN KEY (learner_id,source_id,source_revision)
          REFERENCES source_versions(learner_id,source_id,revision);
        ALTER TABLE observations ADD CONSTRAINT observations_source_json_check
          CHECK (data->>'source_id' IS NOT NULL AND data->>'source_id'=source_id::text);
        ALTER TABLE activities ADD CONSTRAINT activities_source_version_fkey
          FOREIGN KEY (learner_id,source_id,source_revision)
          REFERENCES source_versions(learner_id,source_id,revision);
        ALTER TABLE activities ADD CONSTRAINT activities_source_json_check
          CHECK (data->>'source_id' IS NOT NULL AND data->>'source_id'=source_id::text);
        ALTER TABLE activities ADD COLUMN observation_id uuid;
        ALTER TABLE activities ADD COLUMN observation_revision integer;
        UPDATE activities SET observation_id=(data->>'observation_id')::uuid,
          observation_revision=(data->>'observation_revision')::integer;
        ALTER TABLE activities ADD CONSTRAINT activities_observation_pair_check
          CHECK ((observation_id IS NULL) = (observation_revision IS NULL)
            AND data->>'observation_id' IS NOT DISTINCT FROM observation_id::text
            AND data->>'observation_revision' IS NOT DISTINCT FROM observation_revision::text);
        ALTER TABLE activities ADD CONSTRAINT activities_observation_fkey
          FOREIGN KEY (learner_id,observation_id,observation_revision)
          REFERENCES observations(learner_id,id,revision);

        DROP TABLE source_history;
        DROP INDEX sources_learner_date;
        ALTER TABLE sources DROP COLUMN kind, DROP COLUMN occurred_at,
          DROP COLUMN qualification, DROP COLUMN raw_text, DROP COLUMN expires_at,
          DROP COLUMN fingerprint;
        ALTER TABLE sources ADD CONSTRAINT sources_current_version_fkey
          FOREIGN KEY (learner_id,id,revision)
          REFERENCES source_versions(learner_id,source_id,revision)
          DEFERRABLE INITIALLY DEFERRED;
    """)


def downgrade() -> None:
    # The old global keys and missing evidence revisions cannot represent these states.
    op.execute("""
        LOCK TABLE learners, sources, source_versions, observations, activities, contexts
          IN ACCESS EXCLUSIVE MODE;
        DO $$ BEGIN
          IF EXISTS (SELECT id FROM sources GROUP BY id HAVING count(*)>1)
             OR EXISTS (SELECT id,revision FROM observations GROUP BY id,revision HAVING count(*)>1)
             OR EXISTS (SELECT id,revision FROM activities GROUP BY id,revision HAVING count(*)>1)
          THEN RAISE EXCEPTION 'Stage 2R downgrade: learner-scoped identities collide'; END IF;
          IF EXISTS (
            SELECT 1 FROM observations o JOIN sources s
              ON s.learner_id=o.learner_id AND s.id=o.source_id WHERE s.revision>1
            UNION ALL
            SELECT 1 FROM activities a JOIN sources s
              ON s.learner_id=a.learner_id AND s.id=a.source_id WHERE s.revision>1
          ) THEN
            RAISE EXCEPTION 'Stage 2R downgrade: exact evidence provenance would be lost';
          END IF;
        END $$;
        ALTER TABLE sources DROP CONSTRAINT sources_current_version_fkey;
        ALTER TABLE activities DROP CONSTRAINT activities_observation_fkey;
        ALTER TABLE activities DROP CONSTRAINT activities_observation_pair_check;
        ALTER TABLE activities DROP COLUMN observation_id, DROP COLUMN observation_revision;
        ALTER TABLE activities DROP CONSTRAINT activities_source_version_fkey;
        ALTER TABLE observations DROP CONSTRAINT observations_source_version_fkey;
        ALTER TABLE activities DROP CONSTRAINT activities_source_json_check;
        ALTER TABLE observations DROP CONSTRAINT observations_source_json_check;
        ALTER TABLE activities DROP COLUMN source_revision;
        ALTER TABLE observations DROP COLUMN source_revision;
        ALTER TABLE activities DROP CONSTRAINT activities_pkey;
        ALTER TABLE activities ADD PRIMARY KEY (id,revision);
        ALTER TABLE observations DROP CONSTRAINT observations_pkey;
        ALTER TABLE observations ADD PRIMARY KEY (id,revision);
        ALTER TABLE sources ADD COLUMN kind text, ADD COLUMN occurred_at timestamptz,
          ADD COLUMN qualification text, ADD COLUMN raw_text text,
          ADD COLUMN expires_at timestamptz,
          ADD COLUMN fingerprint text;
        UPDATE sources s SET kind=v.kind,occurred_at=v.occurred_at,
          qualification=v.qualification,raw_text=v.raw_text,expires_at=v.expires_at,
          fingerprint=v.fingerprint FROM source_versions v
          WHERE v.learner_id=s.learner_id AND v.source_id=s.id AND v.revision=s.revision;
        ALTER TABLE sources ALTER COLUMN kind SET NOT NULL,
          ALTER COLUMN qualification SET NOT NULL, ALTER COLUMN expires_at SET NOT NULL,
          ALTER COLUMN fingerprint SET NOT NULL;
        ALTER TABLE sources ADD CONSTRAINT sources_kind_check
          CHECK (kind IN ('lesson','homework','actual_use'));
        ALTER TABLE sources ALTER COLUMN expires_at SET DEFAULT now()+interval '30 days';
        CREATE TABLE source_history (
          source_id uuid NOT NULL,
          learner_id uuid NOT NULL REFERENCES learners(id) ON DELETE CASCADE,
          tutor_id uuid NOT NULL, revision integer NOT NULL, kind text NOT NULL,
          occurred_at timestamptz, qualification text NOT NULL, raw_text text,
          expires_at timestamptz NOT NULL, fingerprint text NOT NULL,
          PRIMARY KEY (source_id,revision)
        );
        INSERT INTO source_history
          SELECT v.source_id,v.learner_id,v.tutor_id,v.revision,v.kind,v.occurred_at,
            v.qualification,v.raw_text,v.expires_at,v.fingerprint FROM source_versions v
          JOIN sources s ON s.learner_id=v.learner_id AND s.id=v.source_id
          WHERE v.revision<>s.revision;
        ALTER TABLE source_history ENABLE ROW LEVEL SECURITY;
        ALTER TABLE source_history FORCE ROW LEVEL SECURITY;
        CREATE POLICY tutor_ownership ON source_history
          USING (tutor_id::text=current_setting('app.tutor_id',true)
            AND EXISTS (SELECT 1 FROM learners WHERE learners.id=source_history.learner_id
              AND learners.tutor_id::text=current_setting('app.tutor_id',true)))
          WITH CHECK (tutor_id::text=current_setting('app.tutor_id',true)
            AND EXISTS (SELECT 1 FROM learners WHERE learners.id=source_history.learner_id
              AND learners.tutor_id::text=current_setting('app.tutor_id',true)));
        GRANT SELECT, INSERT, UPDATE, DELETE ON source_history TO tutor_app;
        DROP TABLE source_versions;
        ALTER TABLE sources DROP CONSTRAINT sources_pkey;
        ALTER TABLE sources ADD PRIMARY KEY (id);
        GRANT DELETE ON sources TO tutor_app;
        ALTER TABLE source_history ADD FOREIGN KEY (source_id)
          REFERENCES sources(id) ON DELETE CASCADE;
        ALTER TABLE observations ADD FOREIGN KEY (source_id) REFERENCES sources(id);
        ALTER TABLE activities ADD FOREIGN KEY (source_id) REFERENCES sources(id);
        CREATE INDEX sources_learner_date ON sources(learner_id,occurred_at DESC,id);
    """)
