"""Versioned teaching bank, separate from private learner evidence."""

from alembic import op

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE teaching_asset_owners (
          id uuid PRIMARY KEY, tutor_id uuid, sharing_permission_ref text,
          CHECK (tutor_id IS NOT NULL OR
                 (sharing_permission_ref IS NOT NULL AND length(sharing_permission_ref) > 0))
        );
        ALTER TABLE teaching_asset_owners ENABLE ROW LEVEL SECURITY;
        ALTER TABLE teaching_asset_owners FORCE ROW LEVEL SECURITY;
        CREATE POLICY owner_read ON teaching_asset_owners FOR SELECT USING (
          current_setting('app.tutor_id', true) <> '' AND
          (tutor_id IS NULL OR tutor_id::text = current_setting('app.tutor_id', true))
        );
        CREATE POLICY owner_insert ON teaching_asset_owners FOR INSERT WITH CHECK (
          tutor_id::text = current_setting('app.tutor_id', true)
        );
        CREATE POLICY owner_delete ON teaching_asset_owners FOR DELETE USING (
          tutor_id::text = current_setting('app.tutor_id', true)
        );
        GRANT SELECT,INSERT,DELETE ON teaching_asset_owners TO tutor_app;
        CREATE TABLE teaching_assets (
          id uuid NOT NULL REFERENCES teaching_asset_owners(id) ON DELETE CASCADE,
          revision integer NOT NULL CHECK (revision > 0),
          data jsonb NOT NULL, reviewed_by text, created_at timestamptz NOT NULL DEFAULT now(),
          embedding vector(384), embedding_revision text,
          PRIMARY KEY (id, revision),
          CHECK ((embedding IS NULL) = (embedding_revision IS NULL))
        );
        ALTER TABLE teaching_assets ENABLE ROW LEVEL SECURITY;
        ALTER TABLE teaching_assets FORCE ROW LEVEL SECURITY;
        CREATE POLICY material_read ON teaching_assets FOR SELECT USING (
          EXISTS (SELECT 1 FROM teaching_asset_owners o WHERE o.id=teaching_assets.id)
        );
        CREATE POLICY material_insert ON teaching_assets FOR INSERT WITH CHECK (
          EXISTS (SELECT 1 FROM teaching_asset_owners o WHERE o.id=teaching_assets.id
            AND o.tutor_id::text = current_setting('app.tutor_id', true))
        );
        CREATE POLICY material_update ON teaching_assets FOR UPDATE USING (
          EXISTS (SELECT 1 FROM teaching_asset_owners o WHERE o.id=teaching_assets.id
            AND o.tutor_id::text = current_setting('app.tutor_id', true))
        ) WITH CHECK (EXISTS (SELECT 1 FROM teaching_asset_owners o WHERE o.id=teaching_assets.id
            AND o.tutor_id::text = current_setting('app.tutor_id', true)));
        CREATE POLICY material_delete ON teaching_assets FOR DELETE USING (
          EXISTS (SELECT 1 FROM teaching_asset_owners o WHERE o.id=teaching_assets.id
            AND o.tutor_id::text = current_setting('app.tutor_id', true))
        );
        GRANT SELECT,INSERT,UPDATE,DELETE ON teaching_assets TO tutor_app;
    """)


def downgrade() -> None:
    op.execute("DROP TABLE teaching_assets; DROP TABLE teaching_asset_owners")
